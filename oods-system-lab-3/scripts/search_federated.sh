count=0
for meta in ../metadata_catalog/*.json
do
    path=$(grep '"data_path"' "$meta" | cut -d '"' -f4)

    if [ -f "../$path" ]; then
        grep "$1" "../$path"
	c=$(grep -c "$1" "../$path")
        count=$((count + c)) 
    else
        echo "Missing dataset: $path"
    fi
done
echo "Total matches: $count"
