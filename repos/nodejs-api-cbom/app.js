const express=require('express'),c=require('./crypto-utils'),app=express();app.use(express.json());
app.get('/health',(q,r)=>r.json({status:'ok'}));
app.post('/hash',(q,r)=>r.json({algorithm:'SHA-256',hash:c.hash(q.body.text)}));
app.post('/password',(q,r)=>r.json({algorithm:'PBKDF2',...c.password(q.body.password)}));
app.post('/encrypt',(q,r)=>r.json({algorithm:'AES-256-GCM',...c.encrypt(q.body.text)}));
app.post('/decrypt',(q,r)=>{try{r.json({text:c.decrypt(q.body)})}catch{r.status(400).json({error:'Invalid ciphertext'})}});
app.post('/sign',(q,r)=>r.json({algorithm:'RSA-2048/SHA-256',...c.sign(q.body.text)}));
app.post('/hmac',(q,r)=>r.json({algorithm:'HMAC-SHA256',value:c.hmac(q.body.text,q.body.secret)}));
if(require.main===module)app.listen(3000,()=>console.log('Listening on 3000'));module.exports=app;
