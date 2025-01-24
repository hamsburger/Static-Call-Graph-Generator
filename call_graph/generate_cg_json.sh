#!/usr/bin/env bash
show_help() {
    ## Generate Help Description
    echo "Use pycg to generate a JSON call graph of codebase"
    echo 
    echo "Syntax: bash generate_webdriver_call_graph.sh [-h|-e|-c] INPUT_REPO_PATH OUTPUT_JSON_PATH"
    echo "Arguments:"
    echo "  INPUT_REPO_PATH -- Local path to code repository. Does not accept online/remote URLs."
    echo "  DIRECTORIES TO FILTER IN INPUT_REPO_PATH."
    echo "  OUTPUT_JSON_PATH -- Path to store output JSON"
    echo 
    echo "Options:"
    echo "  -h, --help          Help Script"
    echo "  -c, --code-folder   Location of Code Folder"
    echo "  -e, --env           Location of Environment File"
    echo "  -j, --json-folder   Location of JSON files"
}

die() {
    ## Fail Code
    printf '%s\n' "$1" >&2
    exit 1
}

position_args=()

## Parse Flags
while [ "$#" -gt 0 ]; do
    case $1 in  -h|-\?|--help)
        show_help
        exit
    ;;
    -e|--env)
        if [ ! $2 ]; then
            die 'ERROR:  "Environment file must not be empty"'
        elif [ ! -e $2 ]; then
            die "ERROR: \"Environment file $2 does not exist/is not a regular file\""
        elif [ ! $2 = *'.env' ]; then
            die 'ERROR: "Environment file should have suffix .env"'
        else
            ## Expand environment variables to this running shell
            source $2
        fi
    ;;
    -c|--code-folder)
        if [ ! $2 ]; then
            die 'ERROR:  "File path must not be empty"'
        elif [ ! -d $2 ]; then
            die "ERROR: \"File path is not a directory/directory $2 does not exist \""
        else
            CODE_FOLDER=$2
            shift 2
        fi
    ;;
    -j|--json-folder)
        if [ ! $2 ]; then
            die 'ERROR:  "File path must not be empty"'
        elif [ ! -d $2 ]; then
            die "ERROR: \"File path is not a directory/directory $2 does not exist \""
        else
            JSON_FOLDER=$2
            shift 2
        fi
    ;;
    *)
       position_args+=("$1")
       shift 1
    ;; 
    esac
done

# If CODE_FOLDER was not specified
if [ ! $CODE_FOLDER ]; then
    INPUT_REPO_PATH=${position_args[0]}
else
    INPUT_REPO_PATH="$CODE_FOLDER/${position_args[0]}"
fi  


if [ ! $JSON_FOLDER ]; then
    OUTPUT_JSON_PATH="${position_args[1]}"
else
    OUTPUT_JSON_PATH="$JSON_FOLDER/${position_args[1]}"
fi

echo "INPUT PATH: $INPUT_REPO_PATH"
echo "OUTPUT PATH: $(find $INPUT_REPO_PATH -name '*.py')"
if python -m pycg --package $INPUT_REPO_PATH $(find $INPUT_REPO_PATH -name "*.py") -o $OUTPUT_JSON_PATH; then
    echo ""
    echo "pycg graph was generated successfully and stored at $OUTPUT_JSON_PATH"
fi 