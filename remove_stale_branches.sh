#!/bin/bash

# Usage : bash remove_stale_branches.sh <days> <tags_to_skip>

# Input validation
if [[ ! "$1" =~ ^[0-9]+$ ]] || [[ "$1" -le 0 ]]; then
    echo "Error: First parameter must be a positive integer (days)"
    exit 1
fi

if [[ ! "$2" =~ ^[0-9]+$ ]] || [[ "$2" -lt 0 ]]; then
    echo "Error: Second parameter must be a non-negative integer (tags_to_skip)"
    exit 1
fi

export IFS=$'\n'

# day in seconds
SECONDS=$((86400*$1))
TIME=$(($(date +%s)-$SECONDS))

OUT=""
# loop for deleting old branches
for i in $(git for-each-ref refs/remotes/origin --sort=committerdate  --format='%(HEAD)%(color:yellow)%(refname:short)%(color:reset) %(color:green)%(committerdate:raw)%(color:reset)')
do
    export IFS=$' '
    elements=($i)    
    if [ $TIME -gt ${elements[1]} ]
    then
        export IFS="/"
	    inner_elements=(${elements[0]})
        if [[ ${inner_elements[1]} != "KEEP"* ]]
        then
            if ! git push origin --delete ${inner_elements[1]} 2>/dev/null; then
                echo "Warning: Failed to delete branch ${inner_elements[1]}"
            else
                OUT="${OUT}, ${inner_elements[1]}"
            fi
        fi
    fi
done

export IFS=$'\n'

#loop for deleting old tags
TO_SKIP=$2
for n in $(git tag --sort=-creatordate)
do
    if [ $TO_SKIP -gt 0 ]
    then
        TO_SKIP=$(( $TO_SKIP-1 ))
    else
        git push origin --delete refs/tags/$n
        OUT="${OUT}, ${n}"
    fi
done

echo ${OUT}
echo ${OUT}
echo "branches=$OUT" >> "$GITHUB_OUTPUT"
