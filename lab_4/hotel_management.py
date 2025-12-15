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

booking_details = [9]


def check_name():
    while True:
        print("\n")
        name = input("ENTER GUEST NAME:")
        is_numeric = name.isdigit()

        if len(name) != 0 and is_numeric:
            return name
        else:
            print("Invalid input! Please input a valid name")
            print(" ")


def check_address():
    while True:
        print("\n")
        address = input("ENTER GUEST ADDRESS:")
        is_numeric = address.isdigit()

        if len(address) and not is_numeric:
            return address
        else:
            print("Invalid input ")
        print(" ")


def check_mobile():
    while True:
        print("\n")
        mobile_no = input("ENTER MOBILE/PHONE NO.:")

        if (mobile_no.isdigit() and
                len(mobile_no) and
                len(mobile_no) == 10):
            return mobile_no
        else:
            print("invalid input ")
        print(" ")


def check_days():
    while True:
        print("\n")
        no_of_days = input("ENTER NO. OF DAYS GUEST WANT TO STAY:")
        is_numeric = no_of_days.isdigit()

        if is_numeric and len(no_of_days):
            return no_of_days
        else:
            print("invalid input ")


def check_payment_method():
    while True:
        print("\n")
        option = input("Enter guest's choice:")
        is_numeric = option.isdigit()

        if len(option) and is_numeric and option in {'1', '2'}:
            option = int(option)
            return option
        else:
            print("invalid input ")


class Guest:
    price = 0
    room = "0"

    def __init__(self):
        self.price = 0
        self.name = " "
        self.address = " "
        self.no_of_days = 0
        self.room = "0"

    def enter_details(self):
        self.name = check_name()
        self.address = check_address()
        self.mobile_no = check_mobile()
        self.no_of_days = int(check_days())

    def select_room_type(self):
        print("\nAvialable room types:")
        for type_id, data in ROOM_CONFIG.items():
            print(f"{type_id}.{data['name']} - Rs.{data['price']}")

        while True:
            choice = input("Enter guest's choice:")
            if choice.isdigit() and int(choice) in ROOM_CONFIG:
                type_id = int(choice)
                break
            else:
                print("invalid input")

        selected_room = ROOM_CONFIG[type_id]
        self.price += selected_room['price'] * self.no_of_days
        booking_details[0] = type_id

    def select_payment_method(self):
        print("1. By cash")
        print("2. By credit/debit card")
        op = check_payment_method()
        if op == 1:
            print("No discount.")
        elif op == 2:
            self.price = self.price - ((self.price * 10) / 100)
            print("Discount of 10%.")
        else:
            print("Invalid option.")

    def generate_bill(self):
        print("\n")
        print("NAME-", self.name)
        print("\n")
        print("ADDRESS-", self.address)
        print("\n")
        print("MOBILE NO.-", self.mobile_no)
        print("\n")
        print("YOUR TOTAL BILL IS Rs.", self.price)
        print("\n")

        room_ids = ROOM_CONFIG[booking_details[0]]['room_ids']

        occupied_rooms = []
        f2 = open("hotel.dat", "rb")
        try:
            while True:
                stored_guest = pickle.load(f2)
                occupied_room_number = stored_guest.room
                occupied_rooms.append(occupied_room_number)
                continue
        except EOFError:
            pass

        for room_number in room_ids:
            if room_number not in occupied_rooms:
                print(self.name, " - room", room_number, "is alloted to you")
                self.room = room_number
                break
            else:
                continue
        self.room = room_number
        print("\n")
        print(" THANK YOU ")
        print(" HOPE YOU WOULD ENJOY OUR SERVICE ")


def main():
    while True:
        print("\n")
        print("1. Check in")
        print("2. Show Guest List")
        print("3. Check out")
        print("4. Get info of guest")
        print("5. EXIT")
        menu_choice = input("Enter choice:")

        if menu_choice == "1":
            new_guest = Guest()
            file_data = open("hotel.dat", "ab")
            new_guest.enter_details()
            new_guest.select_room_type()
            new_guest.select_payment_method()
            new_guest.generate_bill()
            pickle.dump(new_guest, file_data, protocol=2)
            file_data.close()

        elif menu_choice == "2":
            file_data = open("hotel.dat", "rb")
            print("NAME", "\t", "\t", "ROOM NO.")
            try:
                while True:
                    guest_entry = pickle.load(file_data)
                    print(guest_entry.name, "\t", "\t", guest_entry.room)
            except EOFError:
                pass
            file_data.close()

        elif menu_choice == "3":
            print("\n")
            while True:
                room_input = input("ENTER ROOM NO.")
                if len(room_input):
                    break
                else:
                    print("no input found")
                    continue
            room_number = int(room_input)
            file_data = open("hotel.dat", "rb")
            file_data = open("hotel.dat", "ab")
            is_found = 0

            try:
                while True:
                    guest_entry = pickle.load(file_data)
                    if guest_entry.room == room_number:
                        is_found = 1
                        removed_guest_name = guest_entry.name
                        print(" ")
                    else:
                        pickle.dump(guest_entry, file_data)
            except EOFError:
                if is_found == 0:
                    print("NO GUEST IN ROOM ", room_number)
                elif is_found == 1:
                    print("THANK YOU", removed_guest_name, "2 FOR VISTING US")
                    print("HOPE YOU LIKE OUR SERVICE")
                    print("\n")
                pass
            file_data.close()
            file_data.close()
            os.remove("hotel.dat")
            os.rename("hotel.dat", "hotel.dat")

        elif menu_choice == "4":
            file_data = open("hotel.dat", "rb")
            while True:
                room_number = input("ENTER ROOM NO.")
                if len(room_number):
                    break
                else:
                    print("no input found")
                    continue
            room_number = int(room_number)
            try:
                is_found = 0
                while True:
                    guest_entry = pickle.load(file_data)
                    new_guest = guest_entry.room
                    if room_number == new_guest:
                        is_found = 1
                        print("NAME-", "\t", "\t", guest_entry.name)
                        print("\n")
                        print("ADDRESS-", "\t", guest_entry.address)
                        print("\n")
                        print("MOBILE NO.-", "  ", guest_entry.mobile_no)
                        print("\n")
                        print("HIS TOTAL BILL IS Rs.", guest_entry.price)
                    elif EOFError:
                        if is_found == 0:
                            print("NO GUEST IN ROOM ", room_number)
                    else:
                        is_found = 0
                        continue
            except EOFError:
                pass
            file_data.close()

        elif menu_choice == "5":
            break

        else:
            print("invalid choice")
            continue


if __name__ == "__main__":
    main()