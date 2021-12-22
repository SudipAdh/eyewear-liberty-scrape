FILES="./image_work/*.jpeg"
for f in $FILES
do
	aws s3 cp $f s3://liberty-image/images/ --acl public-read
done