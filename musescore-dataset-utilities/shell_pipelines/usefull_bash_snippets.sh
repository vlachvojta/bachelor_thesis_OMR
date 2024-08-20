
# for every dir in the current directory, zip all png files to one central images.zip file
for dir in $(ls -d */ | cut -f1 -d'/'); do \
    echo "Zipping $dir"; \
    cd "$dir" || continue; \
    zip -rg ../images.zip *.png > /dev/null; \
    cd .. ; \
done
