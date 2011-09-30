j=0
find ./Annotations/ -name '*.xml' -printf %h/%f\\n | grep -v ./Annotations/sandbox | while read i; do
      j=$[$j+$(grep -o '<polygon>' "$i" | wc -l)]
      echo $j > counter_tmp
done
cp counter_tmp counter

#find ./Annotations/ -name '*.xml' | xargs grep -o '<polygon>' | wc -l > ./counter_tmp
#cp ./counter_tmp ./counter

#find ./Annotations/ -name '*.xml' | xargs grep -o '<polygon>' | wc -l > ./counter

