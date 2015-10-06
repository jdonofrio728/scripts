# Author: Jacob D'Onofrio
# Date: May 2015

import java.lang.Double as Double
import java.lang.String as String
import java.lang.System as System
import java.lang.Thread as Thread
import java.lang.ThreadGroup as ThreadGroup
import java.lang.Runnable as Runnable
import java.lang.Exception as Exception
import java.lang.ProcessBuilder as ProcessBuilder
import java.net.Socket as Socket
import java.net.Inet4Address as Inet4Address

import java.util.Calendar as Calendar;
import java.util.Collections as Collections
import java.util.ArrayList as ArrayList
import java.util.Properties as Properties
import java.util.concurrent.atomic.AtomicInteger as AtomicInteger

import org.joda.time.DateTime as DateTime
import org.joda.time.format.DateTimeFormat as DateTimeFormat

import sys

class FibThread(Thread):
	_results = None
	_iterations = 5000
	_num = 2500
	_counter = AtomicInteger(0)
	def __init__(self, name=None, i=None, n=None, r=None, counter=None):
		if name != None:
			self.setName(name)
		if i != None:
			self._iterations = i
		if n!= None:
			self._num = n
		if r != None:
			self._resultList = r
		#if counter != None:
			#self._counter = counter
	def run(self):
		try:
			i = 0
			while i < self._iterations:
				self._doFib()
				self._counter.incrementAndGet()
				i = i + 1
		except Exception, e:
			print "Thread failed"
			e.printStackTrace()
		print "Thread " + self.getName() + " complete"
	def _doFibRec(self, num):
		n = num
		if n == 1 or n == 2:
			return 1
		return self._doFibRec(n - 1) + self._doFibRec(n - 2)
	def _doFib(self):
		n = self._num
		if n == 1 or n == 2:
			return 1
		f1 = 1
		f2 = 1
		f = 1
		i = 3
		while i <= n:
			f = f1 + f2
			f1 = f2
			f2 = f
			i = i + 1
		return f

class ResultThread(Thread):
	_exit = False
	_outputFile = "output.csv"
	_freq = 5000
	_counter = None
	_pool = None
	def __init__(self, r=None, counter=None, pool=None):
		self.r = r
		self.formatter = DateTimeFormat.forPattern("MM/dd/yyyy HH:mm:ss")
		if counter:
			self._counter = counter
		if pool:
			self._pool = pool
	def run(self):
		i = 0
		rCount = 0
		outfile = open(self._outputFile, 'w')
		outfile.write("TIMESTAMP,SIZE,THROUGHPUT\n")
		while True:
			if self._exit:
				break
			start = System.currentTimeMillis()
			self.sleep(self._freq)
			total = 0
			for t in self._pool:
				total = total + t._counter.get()
				t._counter.set(0)
			end = System.currentTimeMillis()
			timestamp = DateTime.now()
			elap = float(end - start)
			elap = elap / 1000.0
			#size = self._counter.get()
			throughput = float(total) / elap
			print "Result Update: Size=" + str(total) + ", Throughput=" + str(throughput)
			outfile.write('"'+self.formatter.print(timestamp) + '","'+str(total)+'","'+str(throughput)+'"')
			outfile.flush()
			i = i + 1
	def complete(self):
		self._exit = True

# Main
threadCount = 2
if len(sys.argv) > 1:
	threadCount = int(sys.argv[1])
iterations = 3000000
main = Thread.currentThread()
print "Sleeping for 5 seconds"
main.sleep(5000)

resultList = Collections.synchronizedList(ArrayList())
start = System.currentTimeMillis()
threadList = ArrayList()
i = 0
ai = AtomicInteger(0)
while i < threadCount:
	threadName = "Pooled Thread " + str(i)
	t = FibThread(name=threadName, i=iterations, r=resultList)
	t.start()
	threadList.add(t)
	i = i + 1
resultThread = ResultThread(r=resultList, pool=threadList)
resultThread.start()
print str(threadCount) + " Threads started ..."
for t in threadList:
	t.join()
end = System.currentTimeMillis()
result = end - start
resultThread.complete()
resultThread.join()
# Process results
print "Threads Complete"
print "Time: " + str(result)
print "Done"
