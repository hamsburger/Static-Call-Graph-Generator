#!/usr/bin/env bash
show_help() {
    ## Generate Help Description
    echo "Clone github repo into a specified code-folder, or root directory by default"
    echo 
    echo "Syntax: bash clone_github_repo.sh ONLINE_REPO_PATH"
    echo "Arguments:"
    echo "  ONLINE_REPO_PATH -- URL to Git Repository"
    echo "Options:"
    echo "  -c, --code-folder   Location of Code Folder. Default: ./libraries"
}

die() {
    ## Fail Code
    printf '%s\n' "$1" >&2 
    exit 1
}

position_args=()

## Default Code Folder is Current Directory
CODE_FOLDER="./libraries" 


# $\# checks number of arguments used
while [ "$#" -gt 0 ]; do
    case $1 in  -h|-\?|--help)
        show_help
        exit
    ;;
    ## Get Code Folder
    -c|--code-folder)
        if [ ! $2 ]; then
            die "Code Folder name is empty"
        elif [ ! -d $2 ]; then
            die "Code Folder is not a directory"
        else
            CODE_FOLDER=$2
            shift 2
        fi
    ;;
    *)
        position_args+=("$1")
        shift
    ;;
    esac
done


if [ ! ${position_args[0]} ]; then
    die "You cannot clone an empty repository path!"
fi

echo "Cloning ${position_args[0]}"
(cd $CODE_FOLDER && git clone ${position_args[0]})


