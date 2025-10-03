<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ColdPost</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); min-height:100vh; padding:20px; }
.container { max-width:800px; margin:0 auto; background:white; border-radius:16px; box-shadow:0 20px 60px rgba(0,0,0,0.3); padding:40px; }
h1 { color:#333; margin-bottom:10px; font-size:32px; }
.subtitle { color:#666; margin-bottom:30px; font-size:14px; }
.form-group { margin-bottom:25px; }
label { display:block; margin-bottom:8px; color:#333; font-weight:600; font-size:14px; }
input[type="email"], input[type="password"], input[type="text"], textarea { width:100%; padding:12px; border:2px solid #e0e0e0; border-radius:8px; font-size:14px; transition:border-color 0.3s; }
input:focus, textarea:focus { outline:none; border-color:#667eea; }
textarea { resize:vertical; min-height:150px; font-family:inherit; }
.recipients-section { background:#f8f9fa; padding:20px; border-radius:8px; margin-bottom:25px; }
.recipient-row { display:grid; grid-template-columns:1fr 2fr auto; gap:10px; margin-bottom:10px; align-items:center; }
.recipient-row input { margin-bottom:0; }
.btn { padding:12px 24px; border:none; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; transition:all 0.3s; }
.btn-primary { background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:white; width:100%; font-size:16px; padding:16px; }
.btn-primary:hover { transform:translateY(-2px); box-shadow:0 10px 20px rgba(102,126,234,0.3); }
.btn-secondary { background:#667eea; color:white; font-size:12px; padding:8px 16px; }
.btn-secondary:hover { background:#5568d3; }
.btn-remove { background:#ef4444; color:white; font-size:12px; padding:8px 12px; }
.btn-remove:hover { background:#dc2626; }
.info-box { background:#e0e7ff; border-left:4px solid #667eea; padding:15px; border-radius:8px; margin-bottom:25px; font-size:13px; color:#4c51bf; }
.preview { background:#f8f9fa; border:2px dashed #cbd5e0; border-radius:8px; padding:20px; margin-top:15px; font-size:14px; white-space:pre-wrap; color:#333; }
.status { margin-top:20px; padding:15px; border-radius:8px; display:none; }
.status.success { background:#d1fae5; color:#065f46; border:1px solid #10b981; }
.status.error { background:#fee2e2; color:#991b1b; border:1px solid #ef4444; }
.helper-text { font-size:12px; color:#666; margin-top:5px; }
.attachment-item { display:flex; align-items:center; justify-content:space-between; background:#f8f9fa; padding:10px; border-radius:6px; margin-top:8px; font-size:13px; }
.attachment-info { display:flex; align-items:center; gap:8px; }
.attachment-size { color:#666; font-size:12px; }
.attachment-remove { background:none; border:none; color:#ef4444; cursor:pointer; font-size:18px; padding:0 5px; }
.attachment-remove:hover { color:#dc2626; }
</style>
</head>
<body>
<div class="container">
    <h1>📧 ColdPost</h1>
    <p class="subtitle">Send personalized emails to multiple recipients</p>

    <div class="info-box">
        <strong>💡 How to use:</strong> Use {name} in your email template. It will be replaced with each recipient's name.
    </div>

    <form id="emailForm">
        <div class="form-group">
            <label>Your Email Address</label>
            <input type="email" id="senderEmail" required placeholder="your.email@gmail.com">
            <div class="helper-text">Use App Password if using Gmail</div>
        </div>

        <div class="form-group">
            <label>Email Password / App Password</label>
            <input type="password" id="senderPassword" required placeholder="Enter your password">
        </div>

        <div class="form-group">
            <label>Email Subject</label>
            <input type="text" id="subject" required placeholder="Enter email subject">
        </div>

        <div class="recipients-section">
            <label>Recipients</label>
            <div class="upload-section" style="margin-bottom:15px; display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                <input type="file" id="csvFile" accept=".csv" style="display:none;" onchange="handleCSVUpload(event)">
                <button type="button" class="btn btn-secondary" onclick="document.getElementById('csvFile').click()">📁 Upload CSV File</button>
                <button type="button" class="btn btn-remove" onclick="removeCSV()" id="removeCSVBtn" style="display:none;">🗑️ Remove CSV</button>
                <button type="button" class="btn btn-remove" onclick="clearAllRecipients()">✖️ Clear All</button>
                <span id="csvFileName" style="font-size:12px; color:#666;"></span>
            </div>
            <div id="recipientsList">
                <div class="recipient-row">
                    <input type="text" placeholder="Name" class="recipient-name" required>
                    <input type="email" placeholder="email@example.com" class="recipient-email" required>
                    <button type="button" class="btn btn-remove" onclick="removeRecipient(this)">Remove</button>
                </div>
            </div>
            <button type="button" class="btn btn-secondary" onclick="addRecipient()">+ Add Recipient</button>
            <div class="helper-text" style="margin-top:10px;">
                CSV format: <strong>Option 1:</strong> Name, Email | <strong>Option 2:</strong> First Name, Last Name, Email
            </div>
        </div>

        <div class="form-group">
            <label>Email Template</label>
            <textarea id="template" required placeholder="Hi {name},&#10;&#10;I hope this email finds you well...&#10;&#10;Best regards,&#10;Your Name"></textarea>
            <div class="helper-text">Use {name} where you want to insert the recipient's name</div>
        </div>

        <div class="form-group">
            <label>Attachments (Optional)</label>
            <input type="file" id="attachments" multiple style="display:none;" onchange="handleAttachments(event)">
            <button type="button" class="btn btn-secondary" onclick="document.getElementById('attachments').click()">📎 Add Attachments</button>
            <button type="button" class="btn btn-remove" onclick="clearAttachments()" id="clearAttachmentsBtn" style="display:none; margin-left:10px;">🗑️ Clear Attachments</button>
            <div id="attachmentsList" style="margin-top:10px;"></div>
        </div>

        <div class="form-group">
            <label>Preview (Example with first recipient)</label>
            <div class="preview" id="preview">Your preview will appear here...</div>
        </div>

        <button type="submit" class="btn btn-primary">Send Emails =></button>
    </form>

    <div id="status" class="status"></div>
</div>

<script>
const form = document.getElementById('emailForm');
const preview = document.getElementById('preview');
const template = document.getElementById('template');
const status = document.getElementById('status');
let attachedFiles = [];

// Update preview when template changes
template.addEventListener('input', updatePreview);
document.getElementById('recipientsList').addEventListener('input', updatePreview);

function updatePreview() {
    const templateText = template.value;
    const firstNameInput = document.querySelector('.recipient-name');
    const firstName = firstNameInput ? firstNameInput.value || 'John' : 'John';
    preview.textContent = templateText.replace(/{name}/g, firstName) || 'Your preview will appear here...';
}

function addRecipient() {
    const recipientsList = document.getElementById('recipientsList');
    const newRow = document.createElement('div');
    newRow.className = 'recipient-row';
    newRow.innerHTML = `
        <input type="text" placeholder="Name" class="recipient-name" required>
        <input type="email" placeholder="email@example.com" class="recipient-email" required>
        <button type="button" class="btn btn-remove" onclick="removeRecipient(this)">Remove</button>
    `;
    recipientsList.appendChild(newRow);
}

function removeRecipient(button) {
    const rows = document.querySelectorAll('.recipient-row');
    if (rows.length > 1) button.closest('.recipient-row').remove();
    else alert('You must have at least one recipient!');
}

function handleCSVUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    document.getElementById('csvFileName').textContent = `Loaded: ${file.name}`;
    document.getElementById('removeCSVBtn').style.display = 'inline-block';
    const reader = new FileReader();
    reader.onload = e => parseCSV(e.target.result);
    reader.readAsText(file);
}

function removeCSV() {
    document.getElementById('csvFile').value = '';
    document.getElementById('csvFileName').textContent = '';
    document.getElementById('removeCSVBtn').style.display = 'none';
    status.className = 'status success';
    status.style.display = 'block';
    status.innerHTML = `✅ CSV file removed. Recipients remain in the list.`;
    setTimeout(()=>{status.style.display='none';},2000);
}

function clearAllRecipients() {
    if(!confirm('Are you sure you want to clear all recipients?')) return;
    const recipientsList = document.getElementById('recipientsList');
    recipientsList.innerHTML = `<div class="recipient-row">
        <input type="text" placeholder="Name" class="recipient-name" required>
        <input type="email" placeholder="email@example.com" class="recipient-email" required>
        <button type="button" class="btn btn-remove" onclick="removeRecipient(this)">Remove</button>
    </div>`;
    removeCSV();
    updatePreview();
    status.className = 'status success';
    status.style.display = 'block';
    status.innerHTML = `✅ All recipients cleared!`;
    setTimeout(()=>{status.style.display='none';},2000);
}

function handleAttachments(event) {
    const files = Array.from(event.target.files);
    attachedFiles = [...attachedFiles, ...files];
    displayAttachments();
}

function displayAttachments() {
    const attachmentsList = document.getElementById('attachmentsList');
    const clearBtn = document.getElementById('clearAttachmentsBtn');
    if(attachedFiles.length===0){attachmentsList.innerHTML=''; clearBtn.style.display='none'; return;}
    clearBtn.style.display='inline-block';
    attachmentsList.innerHTML = attachedFiles.map((file,index)=>{
        const sizeKB=(file.size/1024).toFixed(2);
        const sizeMB=(file.size/(1024*1024)).toFixed(2);
        const displaySize=file.size>1024*1024?`${sizeMB} MB`:`${sizeKB} KB`;
        return `<div class="attachment-item">
            <div class="attachment-info">
                <span>📎 ${file.name}</span>
                <span class="attachment-size">(${displaySize})</span>
            </div>
            <button type="button" class="attachment-remove" onclick="removeAttachment(${index})" title="Remove">×</button>
        </div>`;
    }).join('');
}

function removeAttachment(index) {
    attachedFiles.splice(index,1);
    displayAttachments();
}

function clearAttachments() {
    attachedFiles=[];
    document.getElementById('attachments').value='';
    displayAttachments();
    status.className='status success';
    status.style.display='block';
    status.innerHTML='✅ All attachments cleared!';
    setTimeout(()=>{status.style.display='none';},2000);
}

function parseCSV(text){
    const lines=text.split('\n').filter(l=>l.trim());
    if(lines.length===0){alert('CSV empty!'); return;}
    const recipientsList=document.getElementById('recipientsList');
    recipientsList.innerHTML='';
    const firstLine=lines[0].toLowerCase();
    const hasHeader=firstLine.includes('name')||firstLine.includes('email')||firstLine.includes('first');
    const startIndex=hasHeader?1:0;
    const firstDataLine=lines[startIndex]||lines[0];
    const firstMatches=firstDataLine.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g);
    const columnCount=firstMatches?firstMatches.length:0;
    for(let i=startIndex;i<lines.length;i++){
        const line=lines[i].trim(); if(!line) continue;
        const matches=line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g);
        if(!matches) continue;
        let name,email;
        if(columnCount>=3 && matches.length>=3){
            const firstName=matches[0].replace(/^"|"$/g,'').trim();
            const lastName=matches[1].replace(/^"|"$/g,'').trim();
            email=matches[2].replace(/^"|"$/g,'').trim();
            name=`${firstName} ${lastName}`;
        } else if(matches.length>=2){name=matches[0].replace(/^"|"$/g,'').trim(); email=matches[1].replace(/^"|"$/g,'').trim();}
        else continue;
        if(name && email){
            const newRow=document.createElement('div');
            newRow.className='recipient-row';
            newRow.innerHTML=`<input type="text" placeholder="Name" class="recipient-name" value="${name}" required>
            <input type="email" placeholder="email@example.com" class="recipient-email" value="${email}" required>
            <button type="button" class="btn btn-remove" onclick="removeRecipient(this)">Remove</button>`;
            recipientsList.appendChild(newRow);
        }
    }
    if(recipientsList.children.length===0){alert('No valid recipients!'); addRecipient();}
    else {updatePreview(); status.className='status success'; status.style.display='block'; status.innerHTML=`✅ Loaded ${recipientsList.children.length} recipients from CSV!`; setTimeout(()=>{status.style.display='none';},3000);}
}

form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const senderEmail=document.getElementById('senderEmail').value;
    const senderPassword=document.getElementById('senderPassword').value;
    const subject=document.getElementById('subject').value;
    const templateText=document.getElementById('template').value;
    const recipients=[];
    document.querySelectorAll('.recipient-row').forEach(row=>{
        const name=row.querySelector('.recipient-name').value;
        const email=row.querySelector('.recipient-email').value;
        if(name && email) recipients.push({name,email});
    });
    if(!senderEmail||!senderPassword||!subject||!templateText||recipients.length===0){alert("Fill all fields & add at least one recipient!"); return;}
    const formData=new FormData();
    formData.append('senderEmail',senderEmail);
    formData.append('senderPassword',senderPassword);
    formData.append('subject',subject);
    formData.append('template',templateText);
    formData.append('recipients',JSON.stringify(recipients));
    attachedFiles.forEach(file=>formData.append('attachments',file));
    status.style.display='block'; status.className='status'; status.innerHTML='📤 Sending emails...';
    try{
        const response=await fetch('http://localhost:5000/send-emails',{method:'POST',body:formData});
        const result=await response.json();
        if(result.success){
            status.className='status success';
            status.innerHTML=`✅ Emails sent successfully! Sent: ${result.sent}, Failed: ${result.failed}`;
        } else {
            status.className='status error';
            status.innerHTML=`❌ Error: ${result.error}`;
        }
    } catch(err){
        status.className='status error';
        status.innerHTML=`❌ Network or server error: ${err.message}`;
    }
});
</script>
</body>
</html>
