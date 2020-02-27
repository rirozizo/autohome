a=$(cat /var/run/motion/motion.pid)
echo "PID is:"
echo $a
kill $a
