a=$(pidof motion)
echo "PID is:"
echo $a
kill $a

#/etc/init.d/motion stop
