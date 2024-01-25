from tkinter import *       
from tkinter import messagebox, filedialog          
from PIL import Image, ImageTk      
import cv2      
import numpy as np
import math
import sqlite3
import tensorflow as tf 
global global_file_path



root = Tk()
root.title('User Registration')
root.geometry('850x450')
root.configure(bg="#fff")
root.resizable(False, False)


# Create a database connection
conn = sqlite3.connect('user_data.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store user data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name  TEXT,
                    email TEXT,
                    password TEXT
                )''')

def insert_user_data(first_name, last_name, email, password):
    cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, email, password))
    conn.commit()


    #####################################---------------------------------@@Login-Section-Code@@----------------------------------###################################

                                      # code for login pagedef signin():
email_entry = None

def on_enter(event):
    if email_entry.winfo_exists():
        email_entry.delete(0, 'end')

def on_leave(event):
    if email_entry.winfo_exists():
        email = email_entry.get()
         

def signin():
    if email_entry.winfo_exists():
        email = email_entry.get()
        password = code.get()


    # Query the database for the user's credentials
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user_data = cursor.fetchone()
    
    if user_data:
        # If user data is found, show the main application screen
        show_app_screen()
    else:
        messagebox.showerror("Invalid", "Invalid email or password")




    ###---------------------------------------------------------------@@password recovery section @@-----------------------------------------------------------------------
                                            # cod efor password recovery 
def recover_password():
    email_to_recover = email_entry.get()
    
    # Query the database for the user's email
    cursor.execute("SELECT * FROM users WHERE email = ?", (email_to_recover,))
    user_data = cursor.fetchone()
    
    if user_data:
        messagebox.showinfo("Password Recovery", f"Your password is: {user_data[4]}")
    else:
        messagebox.showerror("Error", "User not found")

# show_forgot_password_screen function
def show_forgot_password_screen():
    global email_entry  # Access the global email_entry variable
    forgot_password_screen = Toplevel(root)
    forgot_password_screen.title("Forgot Password")
    forgot_password_screen.geometry('400x200+500+300')
    forgot_password_screen.configure(bg="white")
    forgot_password_screen.resizable(False, False)

    # Label for the main heading
    Label(forgot_password_screen, text='Forgot Password', fg='silver', bg='white',
          font=('Microsoft YaHei UI Light', 18, 'bold')).place(x=45, y=20)

    # Entry field for the user to enter an email
    def on_enter(e):
        email_entry.delete(0, 'end')
    
    def on_leave(e):
        email_entry.delete(0, 'end')

    email_entry = Entry(forgot_password_screen, width=25, fg='silver', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    email_entry.place(x=49, y=80)
    email_entry.insert(0, 'Enter email')
    email_entry.bind('<FocusIn>', on_enter)
    email_entry.bind('<FocusOut>', on_leave)
    Frame(forgot_password_screen, width=300, height=2, bg='silver').place(x=50, y=100)
    
    # Button to recover password
    recover_button = Button(forgot_password_screen, text='Recover Password', font=('Microsoft YaHei UI Light', 11, 'bold'), bg='white', fg='#315c58', border=0,
                            command=recover_password)
    recover_button.place(x=130, y=140)


    ################################------------------------------------@@Sign Up Section@@------------------------------###########################################
                     # code for the new user registration
email_entry = None

def signup():
    def register():
        new_first_name = new_user_first_name.get()
        new_last_name = new_user_last_name.get()
        new_email = email_entry.get()
        new_password = new_user_password.get()
        confirm_password = confirm_new_password.get()

        if new_password == confirm_password:
            insert_user_data(new_first_name, new_last_name, new_email, new_password)
            messagebox.showinfo("Success", "Account created successfully!")
            signup_screen.destroy()
        elif not new_first_name or not new_last_name or not new_email or not new_password or not confirm_password:
            messagebox.showinfo("Empty", "Please enter required data")
        else:
            messagebox.showerror("Invalid", "Passwords do not match")


    signup_screen = Toplevel(root)
    signup_screen.title("Sign Up")
    signup_screen.geometry('350x420+500+300')
    signup_screen.configure(bg="white")
    signup_screen.resizable(False, False)


    # Label for the main heading
    Label(signup_screen, text='Sign Up', fg='silver', bg='white', font=('Microsoft YaHei UI Light', 20, 'bold')).place(x=20, y=20)

    label_font = ('Microsoft YaHei UI Light', 11)

    # Entry field for new user to enter first name
   
    def on_enter(e):
        new_user_first_name.delete(0, 'end')
    
    def on_leave(e):
        new_first_name = new_user_first_name.get()

    new_user_first_name = Entry(signup_screen, width=25, fg='silver', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    new_user_first_name.place(x=50, y=80)
    new_user_first_name.insert(0, 'First name')
    new_user_first_name.bind('<FocusIn>', on_enter)
    new_user_first_name.bind('<FocusOut>', on_leave)
    Frame(signup_screen, width=250, height=2, bg='silver').place(x=50, y=100)


    # Entry field for new user to enter last name
    def on_enter(e):
        new_user_last_name.delete(0, 'end')
    
    def on_leave(e):
        new_last_name = new_user_last_name.get()

    new_user_last_name = Entry(signup_screen, width=25, fg='silver', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    new_user_last_name.place(x=50, y=130)
    new_user_last_name.insert(0, 'Last name')
    new_user_last_name.bind('<FocusIn>', on_enter)
    new_user_last_name.bind('<FocusOut>', on_leave)
    Frame(signup_screen, width=250, height=2, bg='silver').place(x=50, y=150)

    # Entry field for new user to enter email
    def on_enter(e):
        email_entry.delete(0, 'end')
    
    def on_leave(e):
        new_email = email_entry.get()

    email_entry = Entry(signup_screen, width=25, fg='silver', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    email_entry.place(x=50, y=180)
    email_entry.insert(0, 'E-mail Address')
    email_entry.bind('<FocusIn>', on_enter)
    email_entry.bind('<FocusOut>', on_leave)
    Frame(signup_screen, width=250, height=2, bg='silver').place(x=50, y=200)


    # Entry field for new user to enter password

    
    def on_enter(e):
        new_user_password.delete(0, 'end')
    
    def on_leave(e):
        new_password = new_user_password.get()

    new_user_password = Entry(signup_screen, width=25, fg='#C0C0C0', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    new_user_password.place(x=50, y=230)
    new_user_password.insert(0, 'Password')
    new_user_password.bind('<FocusIn>', on_enter)
    new_user_password.bind('<FocusOut>', on_leave)
    Frame(signup_screen, width=250, height=2, bg='#C0C0C0').place(x=50, y=250)



    # Entry field for new user to confirm password

    def on_enter(e):
        confirm_new_password.delete(0, 'end')
    
    def on_leave(e):
        confirm_password = confirm_new_password.get()

    confirm_new_password = Entry(signup_screen, width=25, fg='silver', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    confirm_new_password.place(x=50, y=280)
    confirm_new_password.insert(0, 'Confirm Password')
    confirm_new_password.bind('<FocusIn>', on_enter)
    confirm_new_password.bind('<FocusOut>', on_leave)
    Frame(signup_screen, width=250, height=2, bg='silver').place(x=50, y=300)



    # Button to sign up
    signup_button = Button(signup_screen, text='Sign Up', bg='white', fg='#315c58', font=('Microsoft YaHei UI Light', 20, 'bold'),border=0, cursor='hand2', command=register)
    signup_button.place(x=120, y= 320)




 ###---------------------------------------------------------------@@main system section@@ -----------------------------------------------------------------------

                                # code for main screen where user can detect disease of crops by uploading image

# Create a table to store user data
cursor.execute('''CREATE TABLE IF NOT EXISTS user_data
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   file_path TEXT,
                   selected_option INT,
                   disease_detected TEXT)''')
conn.commit()

# Define the radio buttons globally
tomato_radio = None
potato_radio = None
pepper_radio = None
global global_file_path                           
def show_app_screen():
    def upload_image():
        # Function to upload an image from the user
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            # Load the selected image and display it in the green-colored label
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)

            # Update the label's image and store a reference to prevent garbage collection
            image_label.config(image=photo)
            image_label.image = photo

            # Insert data into the database
            selected_option = option_var.get()
            disease_type = disease_entry.get()
            cursor.execute('INSERT INTO user_data (file_path, selected_option, disease_type) VALUES (?, ?,?)',
                           (file_path, selected_option,disease_type))
                
                           
            conn.commit()

        # Set the global_file_path variable
        global global_file_path
        global_file_path = file_path
        # Use lambda to pass the file_path to detect_disease
        detect_disease_lambda = lambda: detect_disease(global_file_path)
        detect_button.config(command=detect_disease_lambda)

    def detect_disease(file_path):
        global global_file_path
        if not global_file_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return
            # Load the trained model for leaf disease classification


         # Define the classes of diseases
        classes = ["Pepper__bell___Bacterial_spot", "Pepper__bell___healthy", "Potato___Early_blight","Potato___healthy",
               "Potato___Late_blight", "Tomato__Target_Spot", "Tomato__Tomato_mosaic_virus", "Tomato__Tomato_YellowLeaf__Curl_Virus",
               "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_healthy", "Tomato_Late_blight","Tomato_Leaf_Mold",
               "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites_Two_spotted_spider_mite"]
        # Define a function to process the leaf image and predict the disease

        
        model = tf.keras.models.load_model("Automated_disease_detection.h5")


        # Load the image from the file_path
        image = cv2.imread(file_path)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Create a mask for green/yellow/brown colors
        mask_yellow_green = cv2.inRange(hsv, (25, 20, 20), (100, 255, 255))
        mask_brown = cv2.inRange(hsv, (8, 60, 20), (30, 255, 200))
        mask = cv2.bitwise_or(mask_yellow_green, mask_brown)

        # Apply the mask to the image
        result = cv2.bitwise_and(image, image, mask=mask)
        

        # Resize the image  
        result = cv2.resize(result, (256, 256))
        cv2.imshow("Masked image", result)

        # Convert the image to a numpy array
        result = np.array(result)

        # Normalize the pixel values
        result = result / 255.0

        # Add a batch dimension
        result = np.expand_dims(result, axis=0)

        # Predict the disease using the model 
        prediction = model.predict(result)

        # Get the index of the highest probability
        index = np.argmax(prediction)

        # Get the class name
        disease = classes[index]
        print(disease)

        selected_option = option_var.get()  # Get selected option by the user
        disease_type = disease_entry.get()  # Get disease type from user input
        result_text = f"User's Selected option = {selected_option}, User's entered disease type: {disease_type}"

        # Update the database with the detection result
        cursor.execute('UPDATE user_data SET disease_detected = ? WHERE file_path = ?', (result_text, global_file_path))
        conn.commit()

        # Show the disease name on the label
        disease_name.config(text=f"Disease Detected by System: {disease}\n{result_text}")
        #messagebox.showinfo("Disease Detection", "Disease detected in the uploaded image!")
        
    # set background for the screen
    def set_background_image(screen):
        background_image = Image.open("bg4.jpg")
        # Resize the image to match the screen dimensions with antialiasing
        background_image.resize((1440, 959))
        # Create a PhotoImage object from the resized image
        background_photo = ImageTk.PhotoImage(background_image)
        # Create an image item on the Canvas to display the image
        canvas.create_image(0, 0, anchor=NW, image=background_photo)
        canvas.background_photo = background_photo


        
    global screen
    screen = Toplevel(root)
    screen.title("Automated Crop Disease Detection System")
    screen.geometry('1440x959')
    screen.config(bg="#dbd042")
    screen.resizable(True,True)




    # Create a Canvas widget
    canvas = Canvas(screen, bg="#dbd042", width=1440, height=959)
    canvas.pack()

    disease_name = Label(screen, text="")
    disease_name_window = canvas.create_window(770, 650, window=disease_name)


    # Set the background image
    set_background_image(screen)

    # Label for the main heading
    canvas.create_text(320, 100, text='Crop Disease Detection ',
                   font=('Microsoft YaHei UI Light', 30, 'bold'), fill="black")

    # Create a  background rectangle
    background_rect = canvas.create_rectangle(100, 150, 200, 190, fill="#dbd042", outline="#96ad41")

    # Create the text label on top of the rectangle
    canvas.create_text(150, 170, text='Choose', font=('Microsoft YaHei UI Light', 20, 'bold'), fill="white")


    # Load and display crop leaf images
    tomato_leaf = Image.open("tomato.jpg").resize((150, 150))
    tomato_leaf = Image.open("tomato.jpg").resize((150, 150))
    potato_leaf = Image.open("potato.jpg").resize((150, 150))
    pepper_leaf = Image.open("pepper.jpg").resize((150, 150))

    # Convert leaf images to PhotoImage objects
    tomato_photo = ImageTk.PhotoImage(tomato_leaf) 
    potato_photo = ImageTk.PhotoImage(potato_leaf)
    pepper_photo = ImageTk.PhotoImage(pepper_leaf)


    # Create images for crop leaves above radio buttons
    tomato_image = canvas.create_image(170, 300, image=tomato_photo)
    potato_image = canvas.create_image(340, 300, image=potato_photo)
    pepper_image = canvas.create_image(510, 300, image=pepper_photo)
    

    # Radio Buttons for selecting an option
    option_var = IntVar()

    # Create windows for radio buttons on the canvas
    global tomato_radio, potato_radio, pepper_radio
    tomato_radio = Radiobutton(screen, text='Tomato Crop', variable=option_var, value=1, background='#dbd042')
    potato_radio = Radiobutton(screen, text='Potato Crop', variable=option_var, value=2, background='#dbd042')
    pepper_radio = Radiobutton(screen, text='Pepper Crop', variable=option_var, value=3, background='#dbd042')


    tomato_radio_window = canvas.create_window(170, 400, window=tomato_radio)
    potato_radio_window = canvas.create_window(340, 400, window=potato_radio)
    pepper_radio_window = canvas.create_window(510, 400, window=pepper_radio)
    
    #Entry field for the user to enter disease type
    canvas.create_text(190, 450, text='Enter Disease Type:', font=('Microsoft YaHei UI Light', 16, 'bold'), fill="black")
    disease_entry = Entry(screen, highlightthickness=0, bg = '#dbd042')
    disease_entry_window = canvas.create_window(370, 450, window=disease_entry)

    # Button to upload an image
    upload_button = Button(screen, text='Upload image',font=('Microsoft YaHei UI Light', 11, 'bold'),  bg='#dbd042', fg='white', border=2, command=upload_image)
    upload_button_window = canvas.create_window(370, 490, window=upload_button)
    

    # Create a label on the canvas to display the uploaded image
    image_label = Label(screen, bg='green')
    image_label_window = canvas.create_window(370, 650, window=image_label)


    # Button to detect disease
    detect_button = Button(screen ,text='Predict Disease', font=('Microsoft YaHei UI Light', 11, 'bold'), bg='#dbd042', fg='white', border=2, command=detect_disease)
    detect_button_window = canvas.create_window(370, 810, window=detect_button)

    # Global variable to store the uploaded file path
    global_file_path = None

    screen.mainloop()
    


    #######################-------------------------------------------------------------------------------------------------------------------------------------

                        # code for login image that will be shown on the login page.

width = 420
height = 420
img = Image.open("ezd.jpg")
img = img.resize((width, height))
photoImg = ImageTk.PhotoImage(img)
Label(root, image=photoImg, bg='white').place(x=20, y=0)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=450, y=70)

heading = Label(frame, text='Sign in', fg='#315c58', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

    ###-------------------------------------------------------------@@login page section code@@-----------------------------------------------------------------

                            # code for entry of user name each time user try to login the system

def on_enter(e):
    email_entry.delete(0, 'end') 
def on_leave(e):
    email = email_entry.get()
    if email == '':
        email_entry.insert(0, 'E-mail')

email_entry = Entry(frame, width=25, fg='#315c58', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
email_entry.place(x=30, y=80)
email_entry.insert(0, 'E-mail')
email_entry.bind('<FocusIn>', on_enter)
email_entry.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='#315c58').place(x=30, y=107)

    #------------------------------------------------------------------------------------------------------------------------------------------------------------

                        # code for entry of password when user try to login to the system

def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='#315c58', border=0, bg="white", font=('Microsoft YaHei UI Light', 11),show='*')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='#315c58').place(x=30, y=177)

##------------------------------------------------------------------------------------------------------------------------------------------------------------

# sign in button for login each time user open the system.

signin = Button(frame, pady=3, text='Sign in', bg='white', fg='#315c58', border=0, font=('Microsoft YaHei UI Light', 12, 'bold'),cursor='hand2',
                command=signin)
signin.place(x=260, y=200)

label = Label(frame, text="Don't have an account?", fg='#3c543a', bg='white',font=('Microsoft YaHei UI Light', 8, 'bold'))
label.place(x=70, y=270)

# Sign up button for new user registraton.

sign_up = Button(frame, width=6, pady=3, text='Sign up', border=0, font=('Microsoft YaHei UI Light', 12, 'bold'),bg='white', cursor='hand2',
                 fg='#315c58', command=signup)
sign_up.place(x=215, y=260)

# forgot button for password recovery.

forgot_password_button = Button(frame,pady=3,text='Forgot Password', bg='white',border=0,font=('Microsoft YaHei UI Light', 12, 'bold'),cursor='hand2',
                                fg='#315c58',command=show_forgot_password_screen)
forgot_password_button.place(x=25, y=204)

# run main application
root.mainloop()

# Close the database connection when the application exits
conn.close()
