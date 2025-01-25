############################################################################################
#
# 	Author: Harris Zheng
# 	Date: December 21st, 2024
# 	Description: Clone repo, generate cg_json and produce call graph. 
# 
# 	Run remove_repo separately if repo already exists. By default, cloning will fail if 
#   repo already exists.
#
############################################################################################
#
#  REQUIRED_VARS = FILTER ONLINE_REPO_PATH
#  OPTIONAL_VARS = BASE_DIR CODE_FOLDER JSON_FOLDER HTML_FOLDER REPO_NAME OUTPUT_JSON_NAME
#                  STRING_DIRECTORIES
#	
#  Optional Vars can be set if needed. bY default, these values are derived 
#  from ONLINE_REPO_PATH.
#
#  Note: May be easier to specify REPO_NAME instead of ONLINE_REPO_PATH when removing repo
#
############################################################################################

AWS_BUCKET_PATH ?= s3://graphbucket222/
BASE_DIR ?= ./call_graph
CODE_FOLDER ?= ./libraries
JSON_FOLDER ?= ./cg_jsons
HTML_FOLDER ?= ./cg_htmls
STRING_DIRECTORIES ?= ""
REPO_NAME := $(shell basename -s \.git "$$ONLINE_REPO_PATH") # A second $ sign escapes special character $ in Makefile
OUTPUT_JSON_NAME ?= $(shell echo "$(REPO_NAME)" | sed 's/ *$$//')

# Default Makefile executes the first command, so we make our first command 'all'
all: clone_repo generate_cg_json generate_call_graph
all_no_clone: generate_cg_json generate_call_graph
clone_repo:
	@bash $(BASE_DIR)/clone_github_repo.sh $(ONLINE_REPO_PATH) -c $(CODE_FOLDER)

generate_cg_json:
	@bash $(BASE_DIR)/generate_cg_json.sh $(OUTPUT_JSON_NAME) $(OUTPUT_JSON_NAME).json \
		  -c $(CODE_FOLDER) \
		  -j $(JSON_FOLDER) \
		  -s $(STRING_DIRECTORIES)

# Multiline Bash Commands: https://stackoverflow.com/questions/10121182/multi-line-bash-commands-in-makefile
generate_call_graph:
	{ \
	set -e ; \
	python $(BASE_DIR)/generate_call_graph.py \
		-i $(OUTPUT_JSON_NAME).json \
		-o $(OUTPUT_JSON_NAME).html \
		--input_folder $(JSON_FOLDER) \
		--output_folder $(HTML_FOLDER) \
		--filter $(FILTER); \
	}

remove_repo:
	@if [ -d "$(CODE_FOLDER)/$(REPO_NAME)" ]; then \
		rm -rf "$(CODE_FOLDER)/$(REPO_NAME)"; \
	else \
		echo "Repo to remove does not exist!"; \
	fi

sync_with_aws:
	@aws s3 sync $(HTML_FOLDER) $(AWS_BUCKET_PATH)

poetic_setup:
	@poetry init
	@poetry add $(cat requirements.txt)
