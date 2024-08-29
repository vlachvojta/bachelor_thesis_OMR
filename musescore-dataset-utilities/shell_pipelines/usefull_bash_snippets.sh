
# for every dir in the current directory, zip all png files to one central images.zip file
for dir in $(ls -d */ | cut -f1 -d'/'); do \
    echo "Zipping $dir"; \
    cd "$dir" || continue; \
    zip -rg ../images.zip *.png > /dev/null; \
    cd .. ; \
done

# for every dir in the current directory, zip files with chosen suffix (or all using suffix="")
# to zip file with the same name as the directory
suffix=".png"; \
for dir in $(ls -d */ | cut -f1 -d'/'); do \
    echo "Zipping $dir"; \
    zip -r "$dir.zip" $dir/*${suffix} > /dev/null; \
done

# count images in images.zip
unzip -l images.zip | grep png | wc -l
