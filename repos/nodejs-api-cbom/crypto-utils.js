const c=require('node:crypto');
exports.hash=s=>c.createHash('sha256').update(s).digest('hex');
exports.password=s=>{const salt=c.randomBytes(16);return {salt:salt.toString('hex'),hash:c.pbkdf2Sync(s,salt,120000,32,'sha256').toString('hex')}};
exports.encrypt=s=>{const key=c.randomBytes(32),iv=c.randomBytes(12),x=c.createCipheriv('aes-256-gcm',key,iv);return {key:key.toString('base64'),iv:iv.toString('base64'),data:Buffer.concat([x.update(s,'utf8'),x.final()]).toString('base64'),tag:x.getAuthTag().toString('base64')}};
exports.decrypt=p=>{const x=c.createDecipheriv('aes-256-gcm',Buffer.from(p.key,'base64'),Buffer.from(p.iv,'base64'));x.setAuthTag(Buffer.from(p.tag,'base64'));return Buffer.concat([x.update(Buffer.from(p.data,'base64')),x.final()]).toString()};
exports.sign=s=>{const {privateKey,publicKey}=c.generateKeyPairSync('rsa',{modulusLength:2048});const sig=c.sign('sha256',Buffer.from(s),privateKey);return {verified:c.verify('sha256',Buffer.from(s),publicKey,sig),signature:sig.toString('base64')}};
exports.hmac=(s,k)=>c.createHmac('sha256',k).update(s).digest('hex');
