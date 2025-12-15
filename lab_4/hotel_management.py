import os
import pickle


print('-' * 53, "5 STAR HOTEL AND RESORTS", '-' * 53)

ROOM_CONFIG = {
    1: {
        "name": "Delux",
        "price": 2000,
        "room_ids": range(1, 11)
    },
    2: {
        "name": "Semi-Delux",
        "price": 1500,
        "room_ids": range(11, 26)
    },
    3: {
        "name": "General",
        "price": 1000,
        "room_ids": range(26, 46)
    },
    4: {
        "name": "Joint Room",
        "price": 1700,
        "room_ids": range(46, 51)
    }
}


def get_valid_input(prompt, validation_func, error_msg="Invalid input"):
    while True:
        print("\n")
        value = input(prompt)
        if validation_func(value):
            return value
        print(error_msg)


class Guest:
    def __init__(self, name, address, mobile_no, days):
        self.name = name
        self.address = address
        self.mobile_no = mobile_no
        self.days = days
        self.price = 0
        self.room_number = 0
        self.room_type_id = 0

    def set_room_type(self, type_id):
        if type_id in ROOM_CONFIG:
            self.room_type_id = type_id
            self.price += ROOM_CONFIG[type_id]['price'] * self.days

    def apply_payment_method(self, method_id):
        if method_id == 2:
            self.price *= 0.9

    def get_bill_info(self):
        return (
            "\n--- BILL ---\n"
            f"name: {self.name}\n"
            f"address: {self.address}\n"
            f"mobile no: {self.mobile_no}\n"
            f"total cost: {self.price}\n"
            "------"
        )


def register_new_guest():
    name = get_valid_input("Enter name", lambda x: len(x) > 0)
    address = get_valid_input("Enter address", lambda x: len(x) > 0)
    mobile = get_valid_input("Enter mobile no", lambda x: x.isdigit() and
                                                          len(x) == 10)
    days = int(get_valid_input("Enter days", lambda x: x.isdigit() and
                                                       int(x) > 0))

    guest = Guest(name, address, mobile, days)

    print("\nAvailable rooms:")
    for r_id, data in ROOM_CONFIG.items():
        print(f"{r_id}.{data['name']} - Rs. {data['price']}")

    room_choice = int(get_valid_input("Select room type: ",
                                      lambda x: x.isdigit() and
                                                int(x) in ROOM_CONFIG))

    guest.set_room_type(room_choice)

    print("\nPayment method:\n1. Cash\n2. Card (10% discount)")
    pay_method = int(get_valid_input("Select method: ",
                                     lambda x: x in ['1', '2']))

    guest.apply_payment_method(pay_method)

    print(guest.get_bill_info())

    return guest


class HotelData:
    def __init__(self, filename="hotel.dat"):
        self.filename = filename

    def save_guest(self, guest):
        with open(self.filename, "ab") as f:
            pickle.dump(guest, f, protocol=2)

    def get_all_guests(self):
        guests = []
        if not os.path.exists(self.filename):
            return guests

        with open(self.filename, "rb") as f:
            try:
                while True:
                    guests.append(pickle.load(f))
            except EOFError:
                pass
        return guests

    def get_occupied_rooms(self):
        guests = self.get_all_guests()
        return [g.room_number for g in guests]

    def find_guest_by_room(self, room_number):
        guests = self.get_all_guests()
        for g in guests:
            if g.room_number == room_number:
                return g
        return None

    def delete_guest_by_room(self, room_number):
        guests = self.get_all_guests()
        new_list = [g for g in guests if g.room_number != room_number]

        is_deleted = len(guests) != len(new_list)

        if is_deleted:
            with open(self.filename, "wb") as f:
                for g in new_list:
                    pickle.dump(g, f, protocol=2)

        return is_deleted


def main():
    db = HotelData()

    while True:
        print("\n=== HOTEL MANAGEMENT SYSTEM ===")
        print("1. Check in")
        print("2. Show Guest List")
        print("3. Check out")
        print("4. Get info of guest")
        print("5. EXIT")

        menu_choice = get_valid_input("Enter choice: ",
                                      lambda x: x in ['1', '2', '3', '4', '5'])

        if menu_choice == "1":
            new_guest = register_new_guest()

            room_ids = ROOM_CONFIG[new_guest.room_type_id]['room_ids']
            occupied_rooms = db.get_occupied_rooms()

            found = False
            for r in room_ids:
                if r not in occupied_rooms:
                    new_guest.room_number = r
                    print(f"Room {r} allocated successfully!")
                    db.save_guest(new_guest)
                    found = True
                    break

            if not found:
                print("Sorry, no rooms available of this type.")

        elif menu_choice == "2":
            guests = db.get_all_guests()
            print(f"\n{'NAME':<20} {'ROOM NO.':<10}")
            print("-" * 30)
            for guest in guests:
                print(f"{guest.name:<20} {guest.room_number:<10}")

        elif menu_choice == "3":
            room_num = int(
                get_valid_input("ENTER ROOM NO: ", lambda x: x.isdigit()))
            if db.delete_guest_by_room(room_num):
                print(f"Guest checked out from room {room_num}.")
            else:
                print(f"No guest found in room {room_num}.")

        elif menu_choice == "4":
            room_num = int(
                get_valid_input("ENTER ROOM NO: ", lambda x: x.isdigit()))
            guest = db.find_guest_by_room(room_num)
            if guest:
                print(guest.get_bill_info())
            else:
                print("Guest not found.")

        elif menu_choice == "5":
            print("Exiting...")
            break


if __name__ == "__main__":
    # we changed the class structure, old hotel.dat is incompatible.
    if os.path.exists("hotel.dat"):
        try:
            with open("hotel.dat", "rb") as f:
                pickle.load(f)
        except (AttributeError, EOFError, ImportError):
            print("Old database format detected. Resetting database...")
            os.remove("hotel.dat")

    main()