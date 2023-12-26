import pymongo
import flask
from pymongo import MongoClient
from flask import Flask, request, jsonify , session
from bson.objectid import ObjectId
import json


# MongoDB setup
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['DigitalAirlines']
users = db['users']
flights = db['flights']
reservations = db['reservations']

# Set the secret key for the session
app.secret_key = 'digital_airlines2023'

#Register of user
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
       
        # Check if user already exists
        existing_user = users.find_one({'$or': [{'username': data['username']}, {'email': data['email']}]})
        if existing_user:
            return jsonify({'message': 'User with given username or email already exists'}), 409
        else:
            user = {
                "username": data['username'],
                "email": data['email'],
                "password": data['password'],
                "date_of_birth": data['date_of_birth'],
                "country_of_origin": data['country_of_origin'],
                "passport_number": data['passport_number'],
                "user_type": "user"
            }
            result = users.insert_one(user)
            return jsonify(str(result.inserted_id)), 201
    except Exception as e:
        return jsonify({'message': 'An error occurred during user registration'}), 500



#Login of user or admin
@app.route('/login', methods=['POST'])
def login():
    try:

    
        if not session.get('logged_in'):
            data = request.get_json()
            user = users.find_one({"email": data['email']})

            if user and user['password'] == data['password']:
                session['logged_in'] = True
                session['user_id'] = str(ObjectId(user['_id']))
                if user['user_type'] == 'admin':
                    session['user_type'] = 'admin'
                else:
                    session['user_type'] = 'user'
                return jsonify({"message": "Logged in"}), 200
            else:
                return jsonify({"message": "Invalid email or password"}), 401
        else:
            return jsonify({"message": "You have already logged in"}), 409
    except Exception as e:
        return jsonify({'message': 'An error occurred during login'}), 500





   
#Logout of user or admin
@app.route('/logout', methods=['POST'])
def logout():


    if session.get('logged_in'):
        # Clear all session data
        session.clear()  
        return jsonify({'message': 'Logout has been successfully'}), 200
    else:
        return jsonify({'message': 'You have already logout of this platform'}), 400






################# User Pages ######################


#Flight details
@app.route('/flights/<flight_id>', methods=['GET'])
def flight_details(flight_id):
    

    if session.get('logged_in'):

        flight = flights.find_one({"_id":ObjectId(flight_id)})
        if flight:
            flight['_id'] = str(flight['_id'])  
            return jsonify("message:" "Flight with special id found:",flight), 200
        else:
            return jsonify({"message": "Flight not found"}), 404
    else:
         return jsonify({"message":"You must log in to have access in available flights"}),409
    





#Create a reservation of a ticket for user
@app.route('/user_page/reservations', methods=['POST'])
def reservation_ticket():
    
    if  session.get('logged_in'):

        # Get request data
        data = request.get_json()
        
        user_id= session['user_id']
        flight_id = data.get('flight_id')
        name = data.get('name')
        surname = data.get('surname')
        passport_number = data.get('passport_number')
        dob = data.get('dob')
        email = data.get('email')
        ticket_class = data.get('ticket_class')

        # Find the flight
        flight = flights.find_one({"_id": ObjectId(flight_id)})

        if not flight:
            return jsonify({"message": "Flight not found"}), 404

        # Check if there are available tickets for the chosen class
        if ticket_class not in ['business', 'economy']:
            return jsonify({"message": "Invalid ticket class"}), 400


        # Decrease the number of available tickets and if statement for the quantity of these
        if ticket_class == 'business':
            if flight['available_business_tickets'] <= 0:
                return jsonify({"message": "No available business class tickets"}), 400
            else:
                flights.update_one({"_id": ObjectId(flight_id)}, {"$inc": {"available_business_tickets": -1}})
        elif ticket_class == 'economy':
            if flight['available_economy_tickets'] <= 0:
                return jsonify({"message": "No available economy class tickets"}), 400
            else:
                flights.update_one({"_id": ObjectId(flight_id)}, {"$inc": {"available_economy_tickets": -1}})
        else:
            return jsonify({"message": "Invalid ticket class"}), 400
                                
        # Create the booking
        reservations= {
            "user_id":user_id,
            "flight_id": flight_id,
            "name": name,
            "surname": surname,
            "passport_number": passport_number,
            "dob": dob,
            "email": email,
            "ticket_class": ticket_class
        }

         
        # Replace 'db' with your actual database object
        reservations_collection = db.reservations

        # Insert the reservation
        reservations_collection.insert_one(reservations)

       


        return jsonify({"message": "Booking successful"}), 201
    else:
        return jsonify({"message":"You must log in to have access in reservations"}),409
    





#Reservations of a user
@app.route('/user_page/reservations', methods=['GET'])
def get_my_reservations():

    if session.get('logged_in'):
            
            user_id = session['user_id']

            # Replace 'db' with your actual database object
            reservations_collection = db.reservations 
            reservations = reservations_collection.find({'user_id': user_id})

            result_reservations = []
            for reservation in reservations:
                result_reservations.append({
                    'reservation_id': str(reservation['_id']),
                    'flight_id': reservation['flight_id']
                })

            return jsonify(result_reservations),200

    else:
            return jsonify({"message": "No user is currently logged in"}), 403
    








#Reservation details of a flight
@app.route('/user_page/reservations/<reservation_id>', methods=['GET'])
def reservations_details(reservation_id):

    if session.get('logged_in'):

        reservation = reservations.find_one({"_id": ObjectId(reservation_id)})
        if reservation:
            reservation['_id'] = str(reservation['_id'])  
            # Fetch flight details
            flight = flights.find_one({"_id": ObjectId(reservation['flight_id'])})
            if flight:
                #flight['_id'] = str(flight['_id'])
                reservation['flight'] = {
                    'origin': flight['origin'],
                    'destination': flight['destination'],
                    'date': flight['date']
                } 
                del reservation['flight_id']  # Remove the flight_id field from reservation
                del reservation['_id']  # Remove the _id field from reservation
            
            return jsonify(reservation), 200
        else:
            return jsonify({"message": "Booking not found"}), 404
    else:
        return jsonify({"message":"You must log in to have access in reservations"}),409






#Cancel of a reservation
@app.route('/user_page/reservations/<reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):


     if session.get('logged_in'):

        # Find the booking
        reservation = reservations.find_one({"_id": ObjectId(reservation_id)})
        if reservation:
            # Increase the number of available tickets
            ticket_class = reservation['ticket_class']
            flight_id = str(reservation['flight_id'])
            
          

            update_query = {}
            if ticket_class == 'business':
                update_query = {"$inc": {"available_business_tickets": 1}}
            elif ticket_class == 'economy':
                update_query = {"$inc": {"available_economy_tickets": 1}}
            
            # Update the flight document
            flights.update_one({"_id": ObjectId(flight_id)}, update_query)
         
            
            # Delete the booking
            reservations.delete_one({"_id": ObjectId(reservation_id)})

            return jsonify({"message": "Reservation successfully cancelled"}), 200
        else:
            return jsonify({"message": "Reservation not found"}), 404
    
     else:
          return jsonify({"message":"You must log in to cancel a reservation"}),409


#Delete of a user
@app.route('/user_page/delete_user', methods=['DELETE'])
def delete_user():

    

    if session.get('logged_in') and session['user_type'] == 'user':
        users.delete_one({"_id": ObjectId(session['user_id'])})
        session.clear()
        return jsonify({"message": "User account successfully deleted"}), 200
    else:
        return jsonify({"message": "No user is currently logged in"}), 403


################-------------###############


#Welcome of admin page
@app.route('/admin_page', methods=['POST'])
def admin_page():

  

   # Control access to admin page
    if session.get('logged_in') and session['user_type'] == 'admin':
        return jsonify({'message': 'Welcome to admin page!'}), 200
    else:
        return jsonify({'message': 'You dont have access in this page!'}), 403
    

#Welcome of user page
@app.route('/user_page', methods=['POST'])
def user_page():
    # Control access to user page
    if session.get('logged_in') and session['user_type'] == 'user':
        return jsonify({'message': 'Welcome to users page!'}), 200
    else:
        return jsonify({'message': 'You dont have access in this page!'}), 403




#Search of flights
@app.route('/flights', methods=['GET'])
def search_flights():

        if session.get('logged_in'):
                data = request.get_json()

                if 'origin' in data and 'destination' in data and 'date' in data:
                    flights_list = list(flights.find({
                        'origin': data['origin'],
                        'destination': data['destination'],
                        'date': data['date']
                    }))
                elif 'origin' in data and 'destination' in data:
                    flights_list = list(flights.find({
                        'origin': data['origin'],
                        'destination': data['destination']
                    }))
                elif 'date' in data:
                    flights_list = list(flights.find({'date': data['date']}))
                else:
                    flights_list = list(flights.find())

                for flight in flights_list:
                    flight['_id'] = str(flight['_id'])

                return jsonify(flights_list), 200
        else:
             return jsonify({"message":"You must log in to get a flight"}),409






############## Administrator Pages ###########

#Create of a flight
@app.route('/admin_page/flights', methods=['POST'])
def create_flight():
        

  
        if session.get('logged_in') and session['user_type'] == 'admin':

            data = request.get_json()
            available_economy=int(data['economy_tickets'])
            available_business= int(data['business_tickets'])

            flight_id = flights.insert_one({
                "origin": data['origin'],
                "destination": data['destination'],
                "date": data['date'],
                "business_tickets": int(data['business_tickets']),
                "business_cost_ticket": int(data['business_cost_ticket']),
                "economy_tickets": int(data['economy_tickets']),
                "economy_cost_ticket": int(data['economy_cost_ticket']),
                "available_economy_tickets":  available_economy,
                "available_business_tickets": available_business
            }).inserted_id

           
             
            return jsonify({"message": "Flight created successfully", "flight_id": str(flight_id)}), 201
        else:
            return jsonify({"message":"You must log in  to create a flight"}),409

   










#Update of a flight
@app.route('/admin_page/flights/<flight_id>', methods=['PUT'])
def update_flight(flight_id):


    if session.get('logged_in'):
        if  session['user_type'] == 'admin':
            data = request.get_json()
        
            flights.update_one(
                
                    {"_id": ObjectId(flight_id)},
                
                    {"$set": {
                        "business_cost_ticket": data['business_cost_ticket'],
                        "economy_cost_ticket": data['economy_cost_ticket']
                    }}
                )

            return jsonify({"message": "Ticket prices updated successfully"}), 200

        else:    
            return jsonify({"message": "Unauthorized"}), 403
    else:
        return jsonify({"message":"You must log in to update a flight"}),409



#Delete of a flight 
@app.route('/admin_page/flights/<flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    

    if session.get('logged_in'):

        if  session['user_type'] == 'admin':
            # Convert the flight_id to a valid ObjectId
            if ObjectId.is_valid(flight_id):
                flight_id = ObjectId(flight_id)
            else:
                return jsonify({"message": "Invalid flight id"}), 400

            # Check if there are any reservations for the flight
            if reservations.find_one({"flight_id": str(flight_id)}):
                return jsonify({"message": "Cannot delete flight with existing reservations"}), 400

            # Delete the flight
            result = flights.delete_one({"_id": flight_id})

            # If no document was deleted, the flight does not exist
            if result.deleted_count == 0:
                return jsonify({"message": "Flight not found"}), 404

            # Return a success message
            return jsonify({"message": "Flight deleted successfully"}), 200

        else:
            return jsonify({"message": "You must be an admin to delete flights"}), 403
    else:
         return jsonify({"message":"You must log in to update a flight"}),409

        

#Flight details by flight_id
@app.route('/admin_page/flights/<flight_id>', methods=['GET'])
def get_flight_details(flight_id):



    # Find the flight
    flight = flights.find_one({"_id": ObjectId(flight_id)})

    if flight:
        # Get the flight details
        origin = flight['origin']
        destination = flight['destination']
        total_tickets = flight['business_tickets'] + flight['economy_tickets']
        tickets_per_class = {
            'business': flight['business_tickets'],
            'economy': flight['economy_tickets']
        }
        ticket_cost_per_category = {
            'business': flight['business_cost_ticket'],
            'economy': flight['economy_cost_ticket']
        }
        tickets_available = flight['available_business_tickets'] + flight['available_economy_tickets']
        available_tickets_per_class = {
            'business': flight['available_business_tickets'],
            'economy': flight['available_economy_tickets']
        }

        # Get the reservations made for this flight
        flight_reservations = reservations.find({"flight_id": flight_id})

        reservation_details = []
        for reservation in flight_reservations:
            passenger_name = f"{reservation['name']} {reservation['surname']}"
            ticket_category = reservation['ticket_class']
            reservation_details.append({
                'passenger_name': passenger_name,
                'ticket_category': ticket_category
            })

        # Prepare the response
        flight_details = {
            'origin': origin,
            'destination': destination,
            'total_tickets': total_tickets,
            'tickets_per_class': tickets_per_class,
            'ticket_cost_per_category': ticket_cost_per_category,
            'tickets_available': tickets_available,
            'available_tickets_per_class': available_tickets_per_class,
            'reservation_details': reservation_details
        }

        return jsonify(flight_details), 200
    else:
        return jsonify({"message": "Flight not found"}), 404




################-------------################

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)