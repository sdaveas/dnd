const { Document } = require("/document.js");
const d = Document.all.find(x => x.sessionUuid === "3792E01A-FA55-4371-A2C4-49796EF3871A");
if (d) { const t = d.title; d.close(); console.log("closed " + t); }
console.log("remaining: " + Document.all.length);
