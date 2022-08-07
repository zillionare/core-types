#!/bin/bash
if (( $# < 1 ))
then
    echo "版本发布命令，需要配合github actions使用"
    echo "Usage: publish.sh <comments>"
    exit 1
fi

git tag -a "v`poetry version --short`" -m "$1"
git push --tags
