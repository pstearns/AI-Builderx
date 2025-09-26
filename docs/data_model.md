# Data Model

**users**  
id, email unique, password hash, name optional, timestamps.

**labels**  
id, user id, name, color optional, timestamps, unique on user id and name.

**tasks**  
id, user id, title, description optional, priority one of High Medium Low, deadline date, status open or done, label ids list of object id, timestamps.

**Indexes**  
users dot email  
labels dot user id and name  
tasks dot user id  
tasks dot label ids  
tasks dot deadline

**Relations**  
Many to many uses referencing by storing label ids in the task. Use lookup stage for hydrated reads when required.
