print('===============JAVASCRIPT===============');
print('Count of rows in lslMongoDB collection: ' + db.lslMongoDB.count());

db.test.insert({ myfield: 'test1', anotherfield: 'TEST1' });
db.test.insert({ myfield: 'test2', anotherfield: 'TEST2' });

print('===============AFTER JS INSERT==========');
print('Count of rows in lslMongoDB collection: ' + db.lslMongoDB.count());

alltest = db.lslMongoDB.find();
while (alltest.hasNext()) {
  printjson(alltest.next());
}

