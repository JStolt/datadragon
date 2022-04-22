#!/bin/bash
set -e

echo '**************************'
echo '*  GENERATING DB SCHEMA  *'
echo '**************************'
python3 /docker-entrypoint-initdb.d/schema-gen.py | psql -d $POSTGRES_DB -U $POSTGRES_USER -f -

process_file() {
    local file=$1
    local type=$2

    local len=$(expr length $file + 16)
    local str=$(printf "%-${len}s" "*")
    echo "${str// /*}  "
    echo "*  IMPORTING $file  *"
    echo "${str// /*}  "

    filename=$(basename -- "$file")
    filename="${filename%.*}"

    case "$type" in
        "csv")
            psql -a -E -d $POSTGRES_DB -U $POSTGRES_USER -c "\copy ${filename} from $file delimiter ',' $type header NULL as 'null';"
        ;;
        "json")
            psql -a -E -d $POSTGRES_DB -U $POSTGRES_USER -c "\copy ${filename} from $file NULL as 'null';"
        ;;
    esac
}

for file in $(find /data -maxdepth 1 -type f); do
    type=${file##*\.}
    process_file $file $type
done