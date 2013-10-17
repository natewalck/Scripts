#!/bin/bash
# To use this script, simple type ./removeDeprecatedProducts BRANCH_NAME to remove
# all deprecated products from the specified branch.

# Place this script in the same folder as repoutil, otherwise it will not work properly.

# Sanity Check.  Makes sure a branch is specified.
if [[ -z $1 ]]; then
    echo "Please specify a branch"
    exit 1
fi

# Iterates through the output that shows deprecated items in a given branch.
i=0
for item in $(./repoutil --list-branch=${1} | awk '/Deprecated/{ print $1 }'); do
    deprecatedProducts[$i]=$item
    let i++
done

# Removes deprecated products
./repoutil --remove-products="${deprecatedProducts[*]}" $1
