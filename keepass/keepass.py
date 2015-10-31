# Author: Jacob D'Onofrio
# Date: October 2015

import com.hanhuy.keepassj.KdbxFile as KdbxFile
import com.hanhuy.keepassj.PwDatabase as PwDatabase
import com.hanhuy.keepassj.KdbxFormat as KdbxFormat
import com.hanhuy.keepassj.CompositeKey as CompositeKey
import com.hanhuy.keepassj.KcpPassword as KcpPassword
import com.hanhuy.keepassj.IOConnectionInfo as IOConnectionInfo

import java.io.File as File

# Main
print "Here"
dbFile = File("/tmp/test.kdbx")

db = PwDatabase()
key = CompositeKey()
key.AddUserKey(KcpPassword("1234"))
db.Open(IOConnectionInfo.FromPath(dbFile.getAbsolutePath()), key, None)

print str(db.getKeyEncryptionRounds())
i = db.getRootGroup().GetEntries(True).GetAt(0).getStrings().iterator()
while i.hasNext():
	print i.next()

print ""
ps = db.getRootGroup().GetEntries(True).GetAt(0).getStrings().Get("Password")
print ps
print ps.ReadString()

#kdbx = KdbxFile(db)
#kdbx.Load("/home/jdonofrio/Dropbox/Master.kdbx", KdbxFormat.Default, None)
db.Close()

print "Done"
