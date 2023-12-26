#***Digital Airlines System***

**Εισαγωγή:**

Η παρακάτω εργασία περιλαμβάνει την ανάπτυξη ενός web service με χρήση της Python και του Microframework Flask. Το web service παρέχει λειτουργίες για απλούς χρήστες και διαχειριστές. Οι απλοί χρήστες μπορούν να εκτελέσουν λειτουργίες όπως είσοδος στο σύστημα, αναζήτηση πτήσεων, κράτηση εισιτηρίου, ακύρωση κράτησης, και εμφάνιση πληροφοριών κρατήσεων. Οι διαχειριστές έχουν πρόσθετες λειτουργίες, όπως είσοδος στο σύστημα, δημιουργία πτήσεων, ανανέωση τιμών εισιτηρίων, διαγραφή πτήσεων, και αναζήτηση πτήσεων.Ο τρόπος ο οποίος επιτυγχάνεται ολόκληρη η διαδικασία θα αναλυθεί στις επόμενες ενότητες με επεξήγηση του αντίστοιχου κώδικα.

Το web service συνδέεται με μια MongoDB βάση δεδομένων, όπου αποθηκεύονται οι πληροφορίες χρηστών, οι διαθέσιμες πτήσεις και οι κρατήσεις που έχουν γίνει. Η βάση δεδομένων ονομάζεται DigitalAirlines και περιλαμβάνει διάφορα collections για την αποθήκευση των πληροφοριών. Επιπλέον, η εργασία περιλαμβάνει τον containerization του web service με τη χρήση του Docker. Ένα Dockerfile παρέχεται με ακριβείς οδηγίες για τη δημιουργία της εικόνας του web service. Στη συνέχεια, το αρχείο docker-compose.yml δημιουργείται για να συνδέσει τα δύο container, δηλαδή το web service και τη MongoDB, ώστε να μπορούν να τρέχουν μαζί. Με αυτόν τον τρόπο, το web service μπορεί να χρησιμοποιηθεί εύκολα από τους χρήστες για την εκτέλεση των λειτουργιών που περιγράφονται, ενώ η χρήση του Docker εξασφαλίζει την ευκολία της ανάπτυξης και τη διαχείρισης του web service. Τέλος, θα παρουσιαστούν και τα ενδεικτικά αποτελέσματα με χρήση screenshots για την υλοποίηση του πληροφοριακού συστήματος.

**Κεφάλαιο 1:Επεξήγηση κώδικα Python**

**Ενότητα 1.1(Κύριο Μέρος Κώδικα):**

Σε αυτήν την ενότητα παρουσιάζουμε το κύριο σκέλος του κώδικα μας στο οποίο γίνονται τα απαραίτητα imports για να εισάγουμε τις βιβλιοθήκες που θα χρειαστούμε για το πληροφοριακό μας σύστημα. Επιπλέον γίνεται ρύθμιση και σύνδεση με τη βάση δεδομένων MongoDB και καθορίζεται το μυστικό κλειδί για τη συνεδρία του χρήστη.Τέλος, η επόμενη εντολή που βρίσκεται στο τέλος του κύριου μέρος του κώδικα και είναι αυτή που τρέχει το Flask App.Παρακάτω εμφανίζουμε τον κώδικα που μόλις περιγράψαμε:

import pymongo import flask from pymongo import MongoClient from flask import Flask, request, jsonify , session from bson.objectid import ObjectId import json

//MongoDB setup app = Flask(**name**) client = MongoClient('mongodb://mongodb:27017/') db = client['DigitalAirlines'] users = db['users'] flights = db['flights'] reservations = db['reservations']

//Set the secret key for the session app.secret\_key = 'digital\_airlines2023'

//Run Flask App if **name** == '**main**': app.run(debug=True, host='0.0.0.0', port=5000)

**Ενότητα 1.2(Εγγραφή Χρήστη):**

Ο παρακάτω κώδικας παρέχει μια διαδρομή (route) /register που χρησιμοποιείται για την εγγραφή νέου χρήστη στην εφαρμογή.Αναλυτικά:

1)@app.route('/register', methods=['POST']): Ορίζεται μια νέα διαδρομή με τη διεύθυνση '/register' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για την υποβολή των δεδομένων εγγραφής του χρήστη.

2)Εντός της συνάρτησης register(), παίρνονται τα δεδομένα που υποβλήθηκαν στην αίτηση εγγραφής χρήστη με τη χρήση της request.get\_json(). Τα δεδομένα πρέπει να είναι σε μορφή JSON.

3)Ελέγχεται αν ο χρήστης υπάρχει ήδη στη βάση δεδομένων, χρησιμοποιώντας την users.find\_one() για την αναζήτηση ενός χρήστη με το ίδιο όνομα χρήστη ή το ίδιο email. Αν υπάρχει ήδη ένας χρήστης με αυτά τα στοιχεία, επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 409 (Conflict).

4)Αν δεν υπάρχει χρήστης με τα ίδια στοιχεία, δημιουργείται ένα νέο αντικείμενο χρήστη με τα δεδομένα που υποβλήθηκαν στην αίτηση εγγραφής. Το αντικείμενο αυτό περιλαμβάνει τα πεδία "username", "email", "password", "date\_of\_birth", "country\_of\_origin", "passport\_number" και "user\_type".

5)Το νέο αντικείμενο χρήστη εισάγεται στη συλλογή "users" της βάσης δεδομένων χρησιμοποιώντας την users.insert\_one() και επιστρέφεται η απόκριση με το ID του εισαγμένου αντικειμένου ως απόκριση με κωδικό κατάστασης 201 (Created). 6)Αν συμβεί οποιοδήποτε σφάλμα κατά τη διάρκεια της εγγραφής του χρήστη, επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 500 (Internal Server Error).

Aντίστοιχος κώδικας:

#Register of user @app.route('/register', methods=['POST']) def register(): try: data = request.get\_json()

`    `# Check if user already exists

`    `existing\_user = users.find\_one({'$or': [{'username': data['username']}, {'email': data['email']}]})

`    `if existing\_user:

`        `return jsonify({'message': 'User with given username or email already exists'}), 409

`    `else:

`        `user = {

`            `"username": data['username'],

`            `"email": data['email'],

`            `"password": data['password'],

`            `"date\_of\_birth": data['date\_of\_birth'],

`            `"country\_of\_origin": data['country\_of\_origin'],

`            `"passport\_number": data['passport\_number'],

`            `"user\_type": "user"

`        `}

`        `result = users.insert\_one(user)

`        `return jsonify(str(result.inserted\_id)), 201

except Exception as e:

`    `return jsonify({'message': 'An error occurred during user registration'}), 500

ΠΑΡΑΤΗΡΗΣΗ:Ο διαχείριστης είναι ήδη καταχωρημένος στην βάση δεδομένων και δεν απαιτείται να κάνει εγγραφή!!

**Ενότητα 1.3(Σύνδεση χρήστη ή διαχειριστή):**

Ο παρακάτω κώδικας παρέχει μια διαδρομή (route) /login που χρησιμοποιείται για τη σύνδεση ενός χρήστη ή διαχειριστή στην εφαρμογή.Αναλυτικά:

1)@app.route('/login', methods=['POST']): Ορίζεται μια νέα διαδρομή με τη διεύθυνση '/login' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για την υποβολή των δεδομένων σύνδεσης του χρήστη.

2)Ελέγχεται αν ο χρήστης έχει ήδη συνδεθεί με χρήση της session.get('logged\_in'). Αν δεν έχει συνδεθεί, παίρνονται τα δεδομένα που υποβλήθηκαν στην αίτηση σύνδεσης χρήστη με τη χρήση της request.get\_json(). Τα δεδομένα πρέπει να είναι σε μορφή JSON.

3)Αναζητείται ο χρήστης στη βάση δεδομένων χρησιμοποιώντας την users.find\_one() με βάση το email που υποβλήθηκε. Αν βρεθεί ένας χρήστης με το συγκεκριμένο email και ο κωδικός πρόσβασης ταιριάζει, τότε η σύνδεση θεωρείται επιτυχής.

4)Αν η σύνδεση είναι επιτυχής, η μεταβλητή logged\_in της session ορίζεται ως True, και το user\_id και user\_type αποθηκεύονται στην session για χρήση σε άλλες διαδρομές.

5)Αν η σύνδεση δεν είναι επιτυχής, επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 401 (Unauthorized).

7)Αν ο χρήστης έχει ήδη συνδεθεί, επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 409 (Conflict).

8)Αν συμβεί οποιοδήποτε σφάλμα κατά την διάρκεια της σύνδεσης, επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 500 (Internal Server Error).

Aντίστοιχος κώδικας:

#Login of user or admin @app.route('/login', methods=['POST']) def login(): try:

`    `if not session.get('logged\_in'):

`        `data = request.get\_json()

`        `user = users.find\_one({"email": data['email']})

`        `if user and user['password'] == data['password']:

`            `session['logged\_in'] = True

`            `session['user\_id'] = str(ObjectId(user['\_id']))

`            `if user['user\_type'] == 'admin':

`                `session['user\_type'] = 'admin'

`            `else:

`                `session['user\_type'] = 'user'

`            `return jsonify({"message": "Logged in"}), 200

`        `else:

`            `return jsonify({"message": "Invalid email or password"}), 401

`    `else:

`        `return jsonify({"message": "You have already logged in"}), 409

except Exception as e:

`    `return jsonify({'message': 'An error occurred during login'}), 500

**Ενότητα 1.4(Αποσύνδεση χρήστη ή διαχειριστή):**

Ο παραkάtω κώδικας παρέχει μια διαδρομή (route) /logout που χρησιμοποιείται για την αποσύνδεση ενός χρήστη ή διαχειριστή από την εφαρμογή.Αναλυτικά:

1)@app.route('/logout', methods=['POST']): Ορίζεται μια νέα διαδρομή με τη διεύθυνση '/logout' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για την υποβολή αιτήματος αποσύνδεσης.

2)Ελέγχεται αν ο χρήστης έχει συνδεθεί με χρήση της session.get('logged\_in'). Αν έχει συνδεθεί, τα δεδομένα συνεδρίας (session data) διαγράφονται με τη χρήση της session.clear(), και επιστρέφεται ένα μήνυμα επιτυχούς αποσύνδεσης με κωδικό κατάστασης 200 (OK).

3)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 400 (Bad Request) που υποδεικνύει ότι ο χρήστης έχει ήδη αποσυνδεθεί από την πλατφόρμα.

4)Ο κώδικας αυτός χειρίζεται τη λειτουργία της αποσύνδεσης ενός χρήστη ή διαχειριστή και καθαρίζει τα στοιχεία συνεδρίας για τη συγκεκριμένη συνεδρία.

Αντίστοιχος κώδικας:

#Logout of user or admin @app.route('/logout', methods=['POST']) def logout():

if session.get('logged\_in'):

`    `# Clear all session data

`    `session.clear()  

`    `return jsonify({'message': 'Logout has been successfully'}), 200

else:

`    `return jsonify({'message': 'You have already logout of this platform'}), 400

**Ενότητα 1.5(Σελίδα καλωσορίσματος χρήστη):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/user\_page' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για την εμφάνιση της σελίδας χρήστη.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί και αν ο τύπος του χρήστη είναι 'user' χρησιμοποιώντας τις συνθήκες session.get('logged\_in') και session['user\_type'] == 'user'.

2)Αν ο χρήστης έχει συνδεθεί και ο τύπος του χρήστη είναι 'user', τότε επιστρέφεται ένα μήνυμα καλωσορίσματος στη σελίδα των χρηστών με κωδικό κατάστασης 200 (OK).

3)Αν ο χρήστης δεν έχει συνδεθεί ή δεν έχει τον τύπο 'user', επιστρέφεται ένα μήνυμα λάθους με κωδικό κατάστασης 403 (Forbidden) που υποδεικνύει ότι ο χρήστης δεν έχει πρόσβαση σε αυτήν τη σελίδα.

4)Ο κώδικας αυτός χειρίζεται την προβολή της σελίδας χρήστη και ελέγχει την πρόσβαση του χρήστη στη σελίδα με βάση τη συνεδρία και τον τύπο του χρήστη.

Αντίστοιχος κώδικας:

#Welcome of user page @app.route('/user\_page', methods=['POST']) def user\_page(): # Control access to user page if session.get('logged\_in') and session['user\_type'] == 'user': return jsonify({'message': 'Welcome to users page!'}), 200 else: return jsonify({'message': 'You dont have access in this page!'}), 403

**Ενότητα 1.6(Αναζήτηση πτήσεων):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/flights/<flight\_id>' και τη μέθοδο GET. Αυτή η διαδρομή χρησιμοποιείται για να ανακτήσετε τις λεπτομέρειες μιας συγκεκριμένης πτήσης με βάση τον μοναδικό κωδικό της πτήσης (flight\_id).Αναλυτικά:

1)Ελέγχεται αν ο χρήστης ή ο διαχειριστής έχει συνδεθεί, χρησιμοποιώντας τη συνθήκη session.get('logged\_in').

2)Αν ο χρήστης ή ο διαχειριστής έχει συνδεθεί, τότε γίνεται αναζήτηση της πτήσης με τον μοναδικό κωδικό flight\_id στη συλλογή "flights" της βάσης δεδομένων. Αν βρεθεί η πτήση, τότε ο μοναδικός κωδικός της μετατρέπεται σε μια συμβολοσειρά και επιστρέφεται ένα JSON αντικείμενο με μήνυμα ότι η πτήση βρέθηκε και τις λεπτομέρειες της πτήσης, με κωδικό κατάστασης 200 (OK).

3)Αν η πτήση δε βρεθεί, επιστρέφεται ένα JSON αντικείμενο με μήνυμα ότι η πτήση δεν βρέθηκε, με κωδικό κατάστασης 404 (Not Found).

4)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με μήνυμα ότι πρέπει να συνδεθεί για να έχει πρόσβαση στις διαθέσιμες πτήσεις, με κωδικό κατάστασης 409 (Conflict).

5)Ο κώδικας αυτός επιτρέπει στον συνδεδεμένο χρήστη να ανακτήσει τις λεπτομέρειες μιας συγκεκριμένης πτήσης με βάση τον μοναδικό κωδικό της.

Αντίστοιχος κώδικας:

#Flight details @app.route('/flights/<flight\_id>', methods=['GET']) def flight\_details(flight\_id):

if session.get('logged\_in'):

`    `flight = flights.find\_one({"\_id":ObjectId(flight\_id)})

`    `if flight:

`        `flight['\_id'] = str(flight['\_id'])  

`        `return jsonify("message:" "Flight with special id found:",flight), 200

`    `else:

`        `return jsonify({"message": "Flight not found"}), 404

else:

`     `return jsonify({"message":"You must log in to have access in available flights"}),409

**Ενότητα 1.7(Δημιουργία κράτησης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/user\_page/reservations' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για τη δημιουργία μιας κράτησης ενός εισιτηρίου από έναν συνδεδεμένο χρήστη.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί, χρησιμοποιώντας τη συνθήκη session.get('logged\_in').

2)Αν ο χρήστης έχει συνδεθεί, παίρνονται τα δεδομένα του αιτήματος από το JSON αντικείμενο που λαμβάνεται.

3)Παίρνονται οι πληροφορίες της πτήσης και ελέγχεται αν η πτήση υπάρχει. Αν η πτήση δε βρεθεί, επιστρέφεται ένα JSON αντικείμενο με μήνυμα ότι η πτήση δεν βρέθηκε, με κωδικό κατάστασης 404 (Not Found).

4)Ελέγχεται αν η επιλεγμένη κατηγορία εισιτηρίου είναι έγκυρη (business ή economy).

5)Μειώνεται ο αριθμός των διαθέσιμων εισιτηρίων για την επιλεγμένη κατηγορία, ανάλογα με την περίπτωση (business ή economy). Αν δεν υπάρχουν διαθέσιμα εισιτήρια για την επιλεγμένη κατηγορία, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 400 (Bad Request).

6)Δημιουργείται η κράτηση (reservation) με τα στοιχεία του χρήστη και της πτήσης.

7)Η κράτηση εισάγεται στη συλλογή (collection) "reservations" της βάσης δεδομένων.

8)Επιστρέφεται ένα JSON αντικείμενο με μήνυμα επιτυχούς κράτησης, με κωδικό κατάστασης 201 (Created).

9)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 409 (Conflict).

Αντίστοιχος κώδικας:

#Create a reservation of a ticket for user @app.route('/user\_page/reservations', methods=['POST']) def reservation\_ticket():

if  session.get('logged\_in'):

`    `# Get request data

`    `data = request.get\_json()



`    `user\_id= session['user\_id']

`    `flight\_id = data.get('flight\_id')

`    `name = data.get('name')

`    `surname = data.get('surname')

`    `passport\_number = data.get('passport\_number')

`    `dob = data.get('dob')

`    `email = data.get('email')

`    `ticket\_class = data.get('ticket\_class')

`    `# Find the flight

`    `flight = flights.find\_one({"\_id": ObjectId(flight\_id)})

`    `if not flight:

`        `return jsonify({"message": "Flight not found"}), 404

`    `# Check if there are available tickets for the chosen class

`    `if ticket\_class not in ['business', 'economy']:

`        `return jsonify({"message": "Invalid ticket class"}), 400


`    `# Decrease the number of available tickets and if statement for the quantity of these

`    `if ticket\_class == 'business':

`        `if flight['available\_business\_tickets'] <= 0:

`            `return jsonify({"message": "No available business class tickets"}), 400

`        `else:

`            `flights.update\_one({"\_id": ObjectId(flight\_id)}, {"$inc": {"available\_business\_tickets": -1}})

`    `elif ticket\_class == 'economy':

`        `if flight['available\_economy\_tickets'] <= 0:

`            `return jsonify({"message": "No available economy class tickets"}), 400

`        `else:

`            `flights.update\_one({"\_id": ObjectId(flight\_id)}, {"$inc": {"available\_economy\_tickets": -1}})

`    `else:

`        `return jsonify({"message": "Invalid ticket class"}), 400



`    `# Create the booking

`    `reservations= {

`        `"user\_id":user\_id,

`        `"flight\_id": flight\_id,

`        `"name": name,

`        `"surname": surname,

`        `"passport\_number": passport\_number,

`        `"dob": dob,

`        `"email": email,

`        `"ticket\_class": ticket\_class

`    `}



`    `# Replace 'db' with your actual database object

`    `reservations\_collection = db.reservations

`    `# Insert the reservation

`    `reservations\_collection.insert\_one(reservations)




`    `return jsonify({"message": "Booking successful"}), 201

else:

`    `return jsonify({"message":"You must log in to have access in reservations"}),409

**Ενότητα 1.8(Κρατήσεις συνδεδεμένου χρήστη):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/user\_page/reservations' και τη μέθοδο GET. Αυτή η διαδρομή χρησιμοποιείται για την ανάκτηση των κρατήσεων ενός συνδεδεμένου χρήστη.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί, χρησιμοποιώντας τη συνθήκη session.get('logged\_in').

2)Αν ο χρήστης έχει συνδεθεί, παίρνεται ο αναγνωριστικός αριθμός (user\_id) του χρήστη από τη συνεδρία (session).

3)Εντοπίζονται οι κρατήσεις που ανήκουν στον συγκεκριμένο χρήστη, χρησιμοποιώντας την reservations\_collection.find({'user\_id': user\_id}).

4)Οι κρατήσεις που βρέθηκαν μετατρέπονται σε μια λίστα αντικειμένων, και για κάθε κράτηση παίρνονται τα αναγνωριστικά της (reservation\_id) και το flight\_id της πτήσης.

5)Επιστρέφεται η λίστα των κρατήσεων σε μορφή JSON με κωδικό κατάστασης 200 (OK).

6)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 403 (Forbidden).

Αντίστοιχος κώδικας:

#Reservations of a user @app.route('/user\_page/reservations', methods=['GET']) def get\_my\_reservations():

if session.get('logged\_in'):



`        `user\_id = session['user\_id']

`        `# Replace 'db' with your actual database object

`        `reservations\_collection = db.reservations 

`        `reservations = reservations\_collection.find({'user\_id': user\_id})

`        `result\_reservations = []

`        `for reservation in reservations:

`            `result\_reservations.append({

`                `'reservation\_id': str(reservation['\_id']),

`                `'flight\_id': reservation['flight\_id']

`            `})

`        `return jsonify(result\_reservations),200

else:

`        `return jsonify({"message": "No user is currently logged in"}), 403

**Ενότητα 1.9(Λεπτομέρειες κράτησης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/user\_page/reservations/<reservation\_id>' και τη μέθοδο GET. Αυτή η διαδρομή χρησιμοποιείται για την ανάκτηση λεπτομερειών μιας κράτησης για ένα συγκεκριμένο αναγνωριστικό αριθμό κράτησης (reservation\_id).Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί, χρησιμοποιώντας τη συνθήκη session.get('logged\_in').

2)Αν ο χρήστης έχει συνδεθεί, εντοπίζεται η κράτηση με το συγκεκριμένο reservation\_id, χρησιμοποιώντας την reservations.find\_one({"\_id": ObjectId(reservation\_id)}).

3)Αν η κράτηση βρεθεί, μετατρέπεται ο αναγνωριστικός αριθμός της κράτησης (reservation\_id) σε μια συμβολοσειρά και ανακτώνται οι λεπτομέρειες της πτήσης που αντιστοιχεί στην κράτηση.

4)Αν οι λεπτομέρειες της πτήσης βρεθούν, δημιουργείται ένα νέο πεδίο "flight" στην κράτηση, που περιλαμβάνει την προέλευση (origin), τον προορισμό (destination) και την ημερομηνία (date) της πτήσης.

5)Αφαιρούνται τα πεδία "flight\_id" και "\_id" από την κράτηση, καθώς δεν χρειάζονται πλέον.

6)Επιστρέφεται η κράτηση με τις λεπτομέρειες της πτήσης σε μορφή JSON με κωδικό κατάστασης 200 (OK).

7)Αν η κράτηση δεν βρεθεί, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 404 (Not Found).

8)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 409 (Conflict).

Αντίστοιχος κώδικας:

#Reservation details of a flight @app.route('/user\_page/reservations/<reservation\_id>', methods=['GET']) def reservations\_details(reservation\_id):

if session.get('logged\_in'):

`    `reservation = reservations.find\_one({"\_id": ObjectId(reservation\_id)})

`    `if reservation:

`        `reservation['\_id'] = str(reservation['\_id'])  

`        `# Fetch flight details

`        `flight = flights.find\_one({"\_id": ObjectId(reservation['flight\_id'])})

`        `if flight:

`            `#flight['\_id'] = str(flight['\_id'])

`            `reservation['flight'] = {

`                `'origin': flight['origin'],

`                `'destination': flight['destination'],

`                `'date': flight['date']

`            `} 

`            `del reservation['flight\_id']  # Remove the flight\_id field from reservation

`            `del reservation['\_id']  # Remove the \_id field from reservation



`        `return jsonify(reservation), 200

`    `else:

`        `return jsonify({"message": "Booking not found"}), 404

else:

`    `return jsonify({"message":"You must log in to have access in reservations"}),409

**Ενότητα 1.10(Ακύρωση κράτησης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/user\_page/reservations/<reservation\_id>' και τη μέθοδο DELETE. Αυτή η διαδρομή χρησιμοποιείται για την ακύρωση μιας κράτησης με βάση το συγκεκριμένο αναγνωριστικό αριθμό κράτησης (reservation\_id).Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί, χρησιμοποιώντας τη συνθήκη session.get('logged\_in').

2)Αν ο χρήστης έχει συνδεθεί, εντοπίζεται η κράτηση με το συγκεκριμένο reservation\_id, χρησιμοποιώντας την reservations.find\_one({"\_id": ObjectId(reservation\_id)}).

3)Αν η κράτηση βρεθεί, ελέγχεται η κλάση του εισιτηρίου (ticket\_class) και το αντίστοιχο πεδίο διαθέσιμων εισιτηρίων αυξάνεται κατά ένα.

4)Το έγγραφο της πτήσης που σχετίζεται με την κράτηση ενημερώνεται, χρησιμοποιώντας την flights.update\_one({"\_id": ObjectId(flight\_id)}, update\_query), όπου update\_query περιέχει την αύξηση του αντίστοιχου πεδίου διαθέσιμων εισιτηρίων.

5)Η κράτηση διαγράφεται, χρησιμοποιώντας την reservations.delete\_one({"\_id": ObjectId(reservation\_id)}).

6)Επιστρέφεται ένα JSON αντικείμενο με μήνυμα επιτυχίας ακύρωσης κράτησης, με κωδικό κατάστασης 200 (OK).

7)Αν η κράτηση δεν βρεθεί, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 404 (Not Found).

8)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 409 (Conflict).

Αντίστοιχος κώδικας:

#Cancel of a reservation @app.route('/user\_page/reservations/<reservation\_id>', methods=['DELETE']) def cancel\_reservation(reservation\_id):

` `if session.get('logged\_in'):

`    `# Find the booking

`    `reservation = reservations.find\_one({"\_id": ObjectId(reservation\_id)})

`    `if reservation:

`        `# Increase the number of available tickets

`        `ticket\_class = reservation['ticket\_class']

`        `flight\_id = str(reservation['flight\_id'])





`        `update\_query = {}

`        `if ticket\_class == 'business':

`            `update\_query = {"$inc": {"available\_business\_tickets": 1}}

`        `elif ticket\_class == 'economy':

`            `update\_query = {"$inc": {"available\_economy\_tickets": 1}}



`        `# Update the flight document

`        `flights.update\_one({"\_id": ObjectId(flight\_id)}, update\_query)





`        `# Delete the booking

`        `reservations.delete\_one({"\_id": ObjectId(reservation\_id)})

`        `return jsonify({"message": "Reservation successfully cancelled"}), 200

`    `else:

`        `return jsonify({"message": "Reservation not found"}), 404

` `else:

`      `return jsonify({"message":"You must log in to cancel a reservation"}),409

**Ενότητα 1.11(Διαγραφή λογαριασμού χρήστη):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/user\_page/delete\_user' και τη μέθοδο DELETE. Αυτή η διαδρομή χρησιμοποιείται για τη διαγραφή του λογαριασμού χρήστη.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί και είναι χρήστης (όχι διαχειριστής), χρησιμοποιώντας τις συνθήκες session.get('logged\_in') και session['user\_type'] == 'user'.

2)Αν ο χρήστης έχει συνδεθεί ως χρήστης, εκτελείται η διαγραφή του χρήστη από τη συλλογή "users" με βάση το συγκεκριμένο user\_id που αποθηκεύεται στο session.

3)Αποκαθίσταται η συνεδρία (session) με τον καθαρισμό των δεδομένων της.

4)Επιστρέφεται ένα JSON αντικείμενο με μήνυμα επιτυχίας διαγραφής λογαριασμού χρήστη, με κωδικό κατάστασης 200 (OK).

5)Αν ο χρήστης δεν έχει συνδεθεί ως χρήστης, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 403 (Forbidden).

Αντίστοιχος κώδικας:

#Delete of a user @app.route('/user\_page/delete\_user', methods=['DELETE']) def delete\_user():

if session.get('logged\_in') and session['user\_type'] == 'user':

`    `users.delete\_one({"\_id": ObjectId(session['user\_id'])})

`    `session.clear()

`    `return jsonify({"message": "User account successfully deleted"}), 200

else:

`    `return jsonify({"message": "No user is currently logged in"}), 403

**Ενότητα 1.12(Σελίδα καλωσορίσματος διαχειριστή):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/admin\_page' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για την είσοδο στη σελίδα διαχειριστή.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί και είναι διαχειριστής, χρησιμοποιώντας τις συνθήκες session.get('logged\_in') και session['user\_type'] == 'admin'.

2)Αν ο χρήστης έχει συνδεθεί ως διαχειριστής, επιστρέφεται ένα JSON αντικείμενο με μήνυμα καλωσορίσματος στη σελίδα διαχειριστή, με κωδικό κατάστασης 200 (OK).

3)Αν ο χρήστης δεν έχει συνδεθεί ως διαχειριστής, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 403 (Forbidden).

Αντίστοιχος κώδικας:

#Welcome of admin page @app.route('/admin\_page', methods=['POST']) def admin\_page():

#Control access to admin page if session.get('logged\_in') and session['user\_type'] == 'admin': return jsonify({'message': 'Welcome to admin page!'}), 200 else: return jsonify({'message': 'You dont have access in this page!'}), 403

**Ενότητα 1.13(Δημιουργία πτήσης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/admin\_page/flights' και τη μέθοδο POST. Αυτή η διαδρομή χρησιμοποιείται για τη δημιουργία ενός πτήσης από τον διαχειριστή.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί και είναι διαχειριστής, χρησιμοποιώντας τις συνθήκες session.get('logged\_in') και session['user\_type'] == 'admin'.

2)Αν ο χρήστης έχει συνδεθεί ως διαχειριστής, λαμβάνονται τα δεδομένα της πτήσης από το αίτημα POST. Τα δεδομένα αυτά περιλαμβάνουν τις πληροφορίες της πτήσης (αφετηρία, προορισμός, ημερομηνία) και τη διαθεσιμότητα εισιτηρίων για τις κατηγορίες business και economy.

3)Δημιουργείται ένα νέο έγγραφο πτήσης στη συλλογή "flights" της βάσης δεδομένων. Το νέο έγγραφο περιέχει τις πληροφορίες της πτήσης και τη διαθεσιμότητα εισιτηρίων για κάθε κατηγορία.

4)Επιστρέφεται ένα JSON αντικείμενο με μήνυμα επιτυχίας και τον αναγνωριστικό της νέας πτήσης, με κωδικό κατάστασης 201 (Created).

5)Αν ο χρήστης δεν έχει συνδεθεί ως διαχειριστής, επιστρέφεται ένα JSON αντικείμενο με κατάλληλο μήνυμα λάθους, με κωδικό κατάστασης 409 (Conflict).

Αντίστοιχος κώδικας:

#Create of a flight @app.route('/admin\_page/flights', methods=['POST']) def create\_flight():

`    `if session.get('logged\_in') and session['user\_type'] == 'admin':

`        `data = request.get\_json()

`        `available\_economy=int(data['economy\_tickets'])

`        `available\_business= int(data['business\_tickets'])

`        `flight\_id = flights.insert\_one({

`            `"origin": data['origin'],

`            `"destination": data['destination'],

`            `"date": data['date'],

`            `"business\_tickets": int(data['business\_tickets']),

`            `"business\_cost\_ticket": int(data['business\_cost\_ticket']),

`            `"economy\_tickets": int(data['economy\_tickets']),

`            `"economy\_cost\_ticket": int(data['economy\_cost\_ticket']),

`            `"available\_economy\_tickets":  available\_economy,

`            `"available\_business\_tickets": available\_business

`        `}).inserted\_id





`        `return jsonify({"message": "Flight created successfully", "flight\_id": str(flight\_id)}), 201

`    `else:

`        `return jsonify({"message":"You must log in  to create a flight"}),409

**Ενότητα 1.14(Ανανέωση τιμών εισιτηρίων πτήσης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/admin\_page/flights/<flight\_id>' και τη μέθοδο PUT. Αυτή η διαδρομή χρησιμοποιείται για την ενημέρωση των τιμών των εισιτηρίων μιας πτήσης από τον διαχειριστή.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί και είναι διαχειριστής, χρησιμοποιώντας τις συνθήκες session.get('logged\_in') και session['user\_type'] == 'admin'.

2)Αν ο χρήστης έχει συνδεθεί ως διαχειριστής, λαμβάνονται τα νέα δεδομένα για τις τιμές των εισιτηρίων από το αίτημα PUT.

3)Χρησιμοποιώντας τη μέθοδο update\_one() του αντικειμένου συλλογής "flights" στη βάση δεδομένων, ενημερώνονται οι τιμές των εισιτηρίων (business\_cost\_ticket, economy\_cost\_ticket) για την συγκεκριμένη πτήση με βάση το flight\_id που περνιέται ως παράμετρος.

4)Επιστρέφεται ένα JSON αντικείμενο με μήνυμα επιτυχίας, με κωδικό κατάστασης 200 (OK).

5)Αν ο χρήστης δεν έχει συνδεθεί ως διαχειριστής, επιστρέφεται ένα JSON αντικείμενο με μήνυμα αποτροπής πρόσβασης, με κωδικό κατάστασης 403 (Forbidden).

6)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με μήνυμα αποτροπής πρόσβασης και κωδικό κατάστασης 409 (Conflict).

Αντίστοιχος κωδικάς:

#Update of a flight @app.route('/admin\_page/flights/<flight\_id>', methods=['PUT']) def update\_flight(flight\_id):

if session.get('logged\_in'):

`    `if  session['user\_type'] == 'admin':

`        `data = request.get\_json()



`        `flights.update\_one(



`                `{"\_id": ObjectId(flight\_id)},



`                `{"$set": {

`                    `"business\_cost\_ticket": data['business\_cost\_ticket'],

`                    `"economy\_cost\_ticket": data['economy\_cost\_ticket']

`                `}}

`            `)

`        `return jsonify({"message": "Ticket prices updated successfully"}), 200

`    `else:    

`        `return jsonify({"message": "Unauthorized"}), 403

else:

`    `return jsonify({"message":"You must log in to update a flight"}),409

**Ενότητα 1.15(Διαγραφή πτήσης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/admin\_page/flights/<flight\_id>' και τη μέθοδο DELETE. Αυτή η διαδρομή χρησιμοποιείται για τη διαγραφή μιας πτήσης από τον διαχειριστή.Αναλυτικά:

1)Ελέγχεται αν ο χρήστης έχει συνδεθεί και είναι διαχειριστής, χρησιμοποιώντας τις συνθήκες session.get('logged\_in') και session['user\_type'] == 'admin'.

2)Αν ο χρήστης έχει συνδεθεί ως διαχειριστής, ελέγχεται αν το flight\_id είναι έγκυρο. Αν δεν είναι έγκυρο, επιστρέφεται ένα JSON αντικείμενο με μήνυμα λάθους και κωδικό κατάστασης 400 (Bad Request).

3)Ελέγχεται αν υπάρχουν κρατήσεις για τη συγκεκριμένη πτήση. Αν υπάρχουν, επιστρέφεται ένα JSON αντικείμενο με μήνυμα αποτροπής διαγραφής λόγω υπαρκτών κρατήσεων και κωδικό κατάστασης 400 (Bad Request).

4)Αν δεν υπάρχουν κρατήσεις για την πτήση, πραγματοποιείται η διαγραφή της πτήσης με βάση το flight\_id.

5)Επιστρέφεται ένα JSON αντικείμενο με μήνυμα επιτυχίας διαγραφής πτήσης και κωδικό κατάστασης 200 (OK).

6)Αν ο χρήστης δεν έχει συνδεθεί ως διαχειριστής, επιστρέφεται ένα JSON αντικείμενο με μήνυμα αποτροπής πρόσβασης και κωδικό κατάστασης 403 (Forbidden).

7)Αν ο χρήστης δεν έχει συνδεθεί, επιστρέφεται ένα JSON αντικείμενο με μήνυμα αποτροπής πρόσβασης και κωδικό κατάστασης 409 (Conflict).

Αντίστοιχος κώδικας:

#Delete of a flight @app.route('/admin\_page/flights/<flight\_id>', methods=['DELETE']) def delete\_flight(flight\_id):

if session.get('logged\_in'):

`    `if  session['user\_type'] == 'admin':

`        `# Convert the flight\_id to a valid ObjectId

`        `if ObjectId.is\_valid(flight\_id):

`            `flight\_id = ObjectId(flight\_id)

`        `else:

`            `return jsonify({"message": "Invalid flight id"}), 400

`        `# Check if there are any reservations for the flight

`        `if reservations.find\_one({"flight\_id": str(flight\_id)}):

`            `return jsonify({"message": "Cannot delete flight with existing reservations"}), 400

`        `# Delete the flight

`        `result = flights.delete\_one({"\_id": flight\_id})

`        `# If no document was deleted, the flight does not exist

`        `if result.deleted\_count == 0:

`            `return jsonify({"message": "Flight not found"}), 404

`        `# Return a success message

`        `return jsonify({"message": "Flight deleted successfully"}), 200

`    `else:

`        `return jsonify({"message": "You must be an admin to delete flights"}), 403

else:

`     `return jsonify({"message":"You must log in to update a flight"}),409

**Ενότητα 1.16(Εμφάνιση λεπτομερειών πτήσης):**

Ο παρακάτω κώδικας ορίζει μια διαδρομή (route) με τη διεύθυνση '/admin\_page/flights/<flight\_id>' και τη μέθοδο GET. Αυτή η διαδρομή χρησιμοποιείται για την ανάκτηση λεπτομερειών μιας πτήσης βάσει του flight\_id από τον διαχειριστή.Αναλυτικά:

1)Αναζητείται η πτήση βάσει του flight\_id χρησιμοποιώντας τη μέθοδο find\_one του αντικειμένου flights.

2)Αν βρεθεί η πτήση, λαμβάνονται τα αντίστοιχα στοιχεία της πτήσης, όπως το αφετηρία, ο προορισμός, το συνολικό πλήθος εισιτηρίων, το πλήθος εισιτηρίων ανά κατηγορία, το κόστος εισιτηρίων ανά κατηγορία, το διαθέσιμο πλήθος εισιτηρίων και το διαθέσιμο πλήθος εισιτηρίων ανά κατηγορία.

3)Αναζητούνται οι κρατήσεις που έχουν γίνει για αυτήν την πτήση, χρησιμοποιώντας τη μέθοδο find του αντικειμένου reservations με το κριτήριο {"flight\_id": flight\_id}.

4)Οι λεπτομέρειες κάθε κράτησης που βρέθηκε προστίθενται σε μια λίστα αντικειμένων reservation\_details, που περιέχει το όνομα του επιβάτη και την κατηγορία του εισιτηρίου.

5)Οι πληροφορίες της πτήσης και οι λεπτομέρειες των κρατήσεων συγκεντρώνονται σε ένα αντικείμενο flight\_details.

6)Επιστρέφεται το αντικείμενο flight\_details ως απόκριση σε μορφή JSON με κωδικό κατάστασης 200 (ΟΚ).

7)Αν η πτήση δεν βρεθεί, επιστρέφεται ένα JSON αντικείμενο με μήνυμα ότι η πτήση δεν βρέθηκε και κωδικό κατάστασης 404 (Δεν βρέθηκε).

Αντίστοιχος κώδικας:

#Flight details by flight\_id @app.route('/admin\_page/flights/<flight\_id>', methods=['GET']) def get\_flight\_details(flight\_id):

\# Find the flight

flight = flights.find\_one({"\_id": ObjectId(flight\_id)})

if flight:

`    `# Get the flight details

`    `origin = flight['origin']

`    `destination = flight['destination']

`    `total\_tickets = flight['business\_tickets'] + flight['economy\_tickets']

`    `tickets\_per\_class = {

`        `'business': flight['business\_tickets'],

`        `'economy': flight['economy\_tickets']

`    `}

`    `ticket\_cost\_per\_category = {

`        `'business': flight['business\_cost\_ticket'],

`        `'economy': flight['economy\_cost\_ticket']

`    `}

`    `tickets\_available = flight['available\_business\_tickets'] + flight['available\_economy\_tickets']

`    `available\_tickets\_per\_class = {

`        `'business': flight['available\_business\_tickets'],

`        `'economy': flight['available\_economy\_tickets']

`    `}

`    `# Get the reservations made for this flight

`    `flight\_reservations = reservations.find({"flight\_id": flight\_id})

`    `reservation\_details = []

`    `for reservation in flight\_reservations:

`        `passenger\_name = f"{reservation['name']} {reservation['surname']}"

`        `ticket\_category = reservation['ticket\_class']

`        `reservation\_details.append({

`            `'passenger\_name': passenger\_name,

`            `'ticket\_category': ticket\_category

`        `})

`    `# Prepare the response

`    `flight\_details = {

`        `'origin': origin,

`        `'destination': destination,

`        `'total\_tickets': total\_tickets,

`        `'tickets\_per\_class': tickets\_per\_class,

`        `'ticket\_cost\_per\_category': ticket\_cost\_per\_category,

`        `'tickets\_available': tickets\_available,

`        `'available\_tickets\_per\_class': available\_tickets\_per\_class,

`        `'reservation\_details': reservation\_details

`    `}

`    `return jsonify(flight\_details), 200

else:

`    `return jsonify({"message": "Flight not found"}), 404

.

**Κεφάλαιο 2:Δημιουργία DockerFile,docker-compose.yml**

**Ενότητα 2.1(Δημιουργία DockerFile):**

Το παρακάτω είναι ένα αρχείο Dockerfile που ορίζει τη ρύθμιση του περιβάλλοντος εκτέλεσης για την εφαρμογή σας με τη χρήση ενός εικονικού περιβάλλοντος Docker.

Τα βήματα που περιλαμβάνονται είναι τα εξής:

1)Ορίζεται η εικόνα βάσης ως python:3.7-slim-buster, που βασίζεται στην εκδοχή 3.7 της Python και περιέχει μια ελαφριά εγκατάσταση του λειτουργικού συστήματος Debian Buster.

2)Ορίζεται τον κατάλογο εργασίας ως /project, όπου θα τοποθετηθούν τα αρχεία της εφαρμογής.

3)Αντιγράφονται τα αρχεία requirements.txt και e20013\_InfoSys.py στον κατάλογο εργασίας.

4)Εκτελείται η εντολή RUN pip3 install --no-cache-dir -r requirements.txt για να εγκατασταθούν οι απαιτούμενες βιβλιοθήκες Python που καθορίζονται στο αρχείο requirements.txt.

5)Ορίζεται η έκθεση της πόρτας 5000, που είναι η πόρτα στην οποία θα ακούει η εφαρμογή σας.

6)Ορίζονται οι μεταβλητές περιβάλλοντος MONGO\_HOST, MONGO\_PORT και MONGO\_DB για τη ρύθμιση της σύνδεσης με τη βάση δεδομένων MongoDB.

7)Ορίζεται η εντολή CMD για την εκτέλεση της εφαρμογής, όπου το αρχείο e20013\_InfoSys.py είναι το κύριο αρχείο Python που περιέχει τον κώδικα της εφαρμογής σας.

Αντίστοιχος κώδικας:

#Set the base image FROM python:3.7-slim-buster

#Set the working directory WORKDIR /project

COPY requirements.txt .

#Install the required packages RUN pip3 install -r requirements.txt

#Install the required packages RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

#Expose the port EXPOSE 5000

#Set the environment variables ENV MONGO\_HOST=mongodb ENV MONGO\_PORT=27017 ENV MONGO\_DB=DigitalAirlines

#Run the application CMD ["python", "e20013\_InfoSys.py"]

**Ενότητα 2.2(Δημιουργία docker-compose.yml):**

Το παρακάτω αρχείο docker-compose.yml περιγράφει τη διαμόρφωση του περιβάλλοντος εκτέλεσης με τη χρήση του Docker Compose. Οι υπηρεσίες που ορίζονται είναι οι εξής:

1)Η υπηρεσία web που αναπαριστά την εφαρμογή σας. Αυτή η υπηρεσία ορίζεται να χτίζεται χρησιμοποιώντας το Dockerfile που βρίσκεται στον ίδιο φάκελο με το αρχείο docker-compose.yml. Ορίζεται επίσης η προώθηση της πόρτας 5000 από τον εσωτερικό χώρο του εικονικού περιβάλλοντος στον τοπικό χώρο.

2)Η υπηρεσία mongodb που αναπαριστά τη βάση δεδομένων MongoDB. Αυτή η υπηρεσία χρησιμοποιεί την επίσημη εικόνα του MongoDB και ορίζεται να χρησιμοποιεί τον κατάλογο ./data για την αποθήκευση των δεδομένων της βάσης δεδομένων. Επίσης, ορίζεται μια μεταβλητή περιβάλλοντος MONGO\_INITDB\_DATABASE για την αρχική δημιουργία της βάσης δεδομένων με το όνομα DigitalAirlines.

3)Για να εκτελέσετε την εφαρμογή σας με το Docker Compose, ακολουθήστε τα παρακάτω βήματα:

4)Αποθηκεύστε το αρχείο docker-compose.yml στον ίδιο φάκελο με τα υπόλοιπα αρχεία της εφαρμογής.

5)Ανοίξτε μια γραμμή εντολών και πλοηγηθείτε στον φάκελο που περιέχει το αρχείο docker-compose.yml.

6)Εκτελέστε την εντολή docker-compose up για να ξεκινήσει η εκτέλεση των υπηρεσιών. Η εφαρμογή σας θα είναι προσβάσιμη στη διεύθυνση [http://localhost:5000](http://localhost:5000/).

7)Με αυτόν τον τρόπο, το Docker Compose θα χτίσει και θα εκτελέσει την εφαρμογή Flask καθώς και μια εικονική μηχανή MongoDB για τη βάση δεδομένων.

Αντίστοιχος κώδικας:

version: '3'

services: web: build: context: . dockerfile: DockerFile ports: - "5000:5000" volumes: - ./data:/app/data depends\_on: - mongodb

mongodb:

`  `image: mongo:latest

`  `volumes:

`    `- ./data:/data/db

`  `environment:

`    `- MONGO\_INITDB\_DATABASE=DigitalAirlines

**Ενότητα 2.3(Τρόπος εκτέλεσης προγράμματος και αρχείων):**

Ο σωστός τρόπος για να μην έχουμε απώλεια δεδομένων και να τρέξει σωστά ο κώδικας απαιτεί τα ακόλουθα βήματα:

1)Κάνουμε αποσυμπίεση το project.zip

2)Μπαίνοντας απο το terminal στο project path ακολουθούμε τις εντολές της ενότητας 2.4 και τρέχουμε το container έχοντας μεταφέρει τα δεδομένα με επιτυχία.

**Ενότητα 2.4(Τρόπος εκτέλεσης container):**

Οι εντολές που πρέπει να εκτέλεσουμε για να επιτευχθεί το containerize είναι οι ακόλουθες:

Στο project path κάνουμε τις ακόλουθες εντολές:

1)sudo apt-get update 2) sudo apt install -y apt-transport-https ca-certificates curl software-properties-common 3) curl -fsSL <https://download.docker.com/linux/ubuntu/gpg> | sudo apt-key add - 4) sudo add-apt-repository -y "deb [arch=amd64] <https://download.docker.com/linux/ubuntu> $(lsb\_release -cs) stable" 5) sudo apt-get update 6) sudo apt install docker-ce 7)sudo docker-compose build 8)sudo docker compose up 9)sudo iptables -A INPUT -p tcp --dport 27017 -j ACCEPT 10)sudo ufw allow 27017 //Αν θέλουμε να μπούμε στο shell της mongo εκτελούμε την παρακάτω εντολή: 11)sudo docker exec -it (name\_of\_container) mongosh

**Κεφάλαιο 3: Επεξήγηση Postman**

**Ενότητα 3.1(Διαδικασία εγγραφής):**

Για να κάνουμε την εγγραφή του χρήστη τρέχουμε στο postman το <http://localhost:5000/register> χρησιμοποιώντας POST method.Να επισημάνουμε ότι σε περίπτωση λάθους στην επιλογή μεθόδου το postman εμφανίζει μήνυμα λάθους με κωδικό 405.

Τα δεδομένα που πρέπει να εισάγουμε στο πεδίο Body είναι τα εξής:

{ "username": "", "email": "", "password": "", "date\_of\_birth": "", "country\_of\_origin": "", "passport\_number": "", "user\_type": "user" }

Screenshots for register:

![Screenshot (820)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.001.png)

![Screenshot (821)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.002.png)

![Screenshot (822)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.003.png)

**Ενότητα 3.2(Είσοδος χρήστη ή διαχειριστή):**

Για να κάνουμε την σύνδεση του χρήστη ή του διαχειριστή τρέχουμε στο postman το <http://localhost:5000/login> χρησιμοποιώντας POST method.

Τα δεδομένα που πρέπει να εισάγουμε στο πεδίο Body είναι τα εξής:

{ "email": "", "password": "" }

Screenshots for login:

![Screenshot (823)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.004.png)

![Screenshot (824)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.005.png)

![Screenshot (825)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.006.png)

![Screenshot (826)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.007.png)

![Screenshot (838)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.008.png)

![Screenshot (839)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.009.png)

**Ενότητα 3.3(Έξοδος χρήστη ή διαχειριστή):**

Για να κάνουμε την αποσύνδεση του χρήστη ή του διαχειριστή τρέχουμε στο postman το <http://localhost:5000/logout> χρησιμοποιώντας POST method.Πατώντας απλά send είμαστε έτοιμοι για να λάβουμε την απάντηση.

Screenshots for logout:

![Screenshot (851)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.010.png)

![Screenshot (852)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.011.png)

**Ενότητα 3.4(Καλοσώρισμα χρήστη ):**

Για να μπούμε στην σελίδα καλοσωρίσματος χρήστη τρέχουμε στο postman το <http://localhost:5000/user_page> χρησιμοποιώντας POST method.Πατώντας απλά send είμαστε έτοιμοι για να λάβουμε την απάντηση.

Screenshots for user\_page:

![Screenshot (827)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.012.png)

**Ενότητα 3.5(Καλοσώρισμα διαχειριστή ):**

Για να μπούμε στην σελίδα καλοσωρίσματος χρήστη τρέχουμε στο postman το <http://localhost:5000/admin_page> χρησιμοποιώντας POST method.Πατώντας απλά send είμαστε έτοιμοι για να λάβουμε την απάντηση.

Screenshots for admin\_page:

![Screenshot (828)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.013.png)

![Screenshot (840)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.014.png)

**Ενότητα 3.6(Αναζήτηση πτήσεων ):**

Για να μπούμε στην σελίδα αναζήτησης πτήσεων τρέχουμε στο postman το <http://localhost:5000/flights> χρησιμοποιώντας GET method.Ανάλογα το body που θα βάλουμε θα εμφανίσει με αντίστοιχο τρόπο τις πτήσεις.

Screenshots for search\_flights:

![Screenshot (829)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.015.png)

![Screenshot (830)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.016.png)

**Ενότητα 3.7(Δημιουργία κράτησης):**

Για να μπούμε στην σελίδα δημιορυγίας κράτησης τρέχουμε στο postman το <http://localhost:5000/user_page/reservations> χρησιμοποιώντας POST method.

Το body που πρέπει να εισαχθεί για την σωστή εκτέλεση της κράτησης είναι το εξής:

{ "flight\_id": "", "name": "", "surname": "", "passport\_number": "", "dob": "", "email": "", "ticket\_class": "" }

Screenshots for reservation\_ticket:

![Screenshot (833)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.017.png)

![Screenshot (834)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.018.png)

**Ενότητα 3.8(Εμφάνιση κρατήσεων συνδεδεμένου χρήστη):**

Για να μπούμε στην σελίδα εμφάνιση κράτησης του συνδεδεμένου χρήστη τρέχουμε στο postman το <http://localhost:5000/user_page/reservations> χρησιμοποιώντας αυτή την φορά GET method.

Δεν χρειάζεται να εισάγουμε δεδομένα το user\_id μπαίνει αυτόματα μετα την επιτυχή σύνδεση και με βάση αυτό γίνεται η αναζήτηση της κράτησης.

Screenshots for reservation\_userid:

![Screenshot (850)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.019.png)

**Ενότητα 3.9(Εμφάνιση λεπτομερειών κράτησης):**

Για να μπούμε στην σελίδα εμφάνιση λεπτομερειών κράτησης τρέχουμε στο postman το <http://localhost:5000/user_page/reservations/><reservation\_id> χρησιμοποιώντας GET method.

Για την επιτυχή ολοκλήρωση αυτής της διαδικασίας πρέπει να εισάγουμε ένα <reservation\_id> την ώρα που τρέχουμε την σελίδα.

Screenshots for reservation\_details:

![Screenshot (835)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.020.png)

![Screenshot (836)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.021.png)

**Ενότητα 3.10(Ακύρωση κράτησης):**

Για να μπούμε στην σελίδα ακύρωσης κράτησης τρέχουμε στο postman το <http://localhost:5000/user_page/reservations/><reservation\_id> χρησιμοποιώντας DELETE method. Για την επιτυχή ολοκλήρωση αυτής της διαδικασίας πρέπει να εισάγουμε ένα <reservation\_id> την ώρα που τρέχουμε την σελίδα.

Screenshots for cancel\_reservation:

![Screenshot (837)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.022.png)

**Ενότητα 3.11(Διαγραφή λογαριασμού χρήστη):**

Για να μπούμε στην σελίδα διαγραφής λογαριασμού χρήστη τρέχουμε στο postman το <http://localhost:5000/user_page/delete_user> χρησιμοποιώντας DELETE method.Δεν χρειάζεται να εισάγουμε κάτι για να επιτευχθεί η διαδικασία αρκεί να είμαστε συνδεμένοι και να έχουμε συνδεθεί ως χρήστες.

Screenshots for delete\_user:

![Screenshot (853)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.023.png)

**Ενότητα 3.12(Δημιουργία πτήσης):**

Για να μπούμε στην σελίδα δημιορυγίας κράτησης τρέχουμε στο postman το <http://localhost:5000/admin_page/flights> χρησιμοποιώντας POST method.

Το body που πρέπει να εισαχθεί για την σωστή εκτέλεση της πτήσης είναι το εξής:

{ "origin": "", "destination": "", "date": "", "business\_tickets": "", "business\_cost\_ticket": "", "economy\_tickets": "", "economy\_cost\_ticket": "" }

Screenshots for create\_flights:

![Screenshot (841)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.024.png)

**Ενότητα 3.13(Ανανέωση τιμών εισιτηρίων πτήσης):**

Για να μπούμε στην σελίδα ανανέωσης τιμών εισιτηρίων τρέχουμε στο postman το <http://localhost:5000/admin_page/flights/><flight\_id> χρησιμοποιώντας PUT method.

Αρχικά εισάγουμε το <flight\_id> για να βρούμε την αντίστοιχη πτήση.

Στην συνέχεια το body που πρέπει να εισαχθεί για την σωστή εκτέλεση της ανανέωσης τιμών εισιτηρίων πτήσης είναι το εξής:

{ "business\_cost\_ticket": "", "economy\_cost\_ticket": "" }

Screenshots for update\_flights:

![Screenshot (842)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.025.png)

**Ενότητα 3.14(Διαγραφή πτήσης):**

Για να μπούμε στην σελίδα διαγραφής λογαριασμού χρήστη τρέχουμε στο postman το <http://localhost:5000/admin_page/flights/><flight\_id> χρησιμοποιώντας DELETE method.Για την επίτευξη της διαγραφής εισάγουμε το <flight\_id> για να βρούμε την αντίστοιχη πτήση.

Screenshots for delete\_flights:

![Screenshot (846)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.026.png)

![Screenshot (847)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.027.png)

**Ενότητα 3.15(Εμφάνιση λεπτομερειών πτήσης):**

Για να μπούμε στην σελίδα εμφάνισης λεπτομερειών πτήσης τρέχουμε στο postman το <http://localhost:5000/admin_page/flights/><flight\_id> χρησιμοποιώντας GET method.Για την επίτευξη της εμφάνισης εισάγουμε το <flight\_id> για να βρούμε την αντίστοιχη πτήση.

Screenshots for get\_flights\_details:

![Screenshot (843)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.028.png)

![Screenshot (844)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.029.png)

![Screenshot (845)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.030.png)

**Ενότητα 3.16(Αναζήτηση πτήσεων με βάση τον κωδικό ):**

Για να μπούμε στην σελίδα αναζήτησης πτήσεων με βάση μόνο τον κωδικό τρέχουμε στο postman το <http://localhost:5000/flights/><flight\_id> χρησιμοποιώντας GET method.

Screenshots for get\_flights\_id:

![Screenshot (831)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.031.png)

![Screenshot (832)](Aspose.Words.c385cefe-883e-413c-8ad4-2b6fbc855785.032.png)

**Βιβλιογραφία εργασίας:**

1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/Lab%20Extra%20Materials%20-%20Postman.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/Lab%201%20-%20Intro%20to%20Python%20and%20SOA.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/%CE%95%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CC%81%CF%81%CE%B9%CE%BF%202.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/Lab%203%20-%20MongoDB%20and%20Flask.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/Lab%204%20-%20MongoDB%20and%20Flask%20.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/Lab%205%20-%20MongoDB%2C%20Flask%20and%20Docker%20Compose.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%AF%CF%89%CE%BD/Lab%206%20-%20Web%20Service%20Containerization%20-%20Docker%20compose%20.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B4%CE%B9%CE%B1%CE%BB%CE%AD%CE%BE%CE%B5%CF%89%CE%BD/InfoSys%209%20-%202022-2023.pdf>
1. <https://aristarchus.ds.unipi.gr/modules/document/file.php/DS-COURSES-SEM138/%CE%94%CE%B9%CE%B1%CF%86%CE%AC%CE%BD%CE%B5%CE%B9%CE%B5%CF%82%20%CE%B4%CE%B9%CE%B1%CE%BB%CE%AD%CE%BE%CE%B5%CF%89%CE%BD/InfoSys%2010%20-%202022-2023.pdf>

