import tweetpy_functions

exit = "false"
while exit == "false":

    command = input("Please input your command. Type list for list of commands and help for description of what the commands do: ")

    if command == "list":
        print("The list of available commands is: author, auto, collect, list, help, and exit. ")
        continue
    elif command == "author":
        tweetpy_functions.author_tweet()
        continue
    elif command == "auto":
        tweetpy_functions.auto()
        continue
    elif command == "collect":
        tweetpy_functions.collect_profiles()
        continue
    elif command == "exit":
        exit = "true"
        print("Exiting process. Thank you")
        continue
    elif command == "help":
        print("author:  Author a tweet, auto: Begin auto tweeting or auto collecting, collect: Begin tweet collection process, list: list all commands")
    else:
        print("Command not recognized.  Please try again")
        continue