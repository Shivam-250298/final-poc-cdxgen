const test=require('node:test'),a=require('node:assert/strict'),c=require('../crypto-utils');
test('hash',()=>a.equal(c.hash('hello').length,64));
test('PBKDF2',()=>a.notEqual(c.password('demo').salt,c.password('demo').salt));
test('AES',()=>a.equal(c.decrypt(c.encrypt('hello')),'hello'));
test('RSA',()=>a.equal(c.sign('hello').verified,true));
test('HMAC',()=>a.equal(c.hmac('hello','key'),c.hmac('hello','key')));
