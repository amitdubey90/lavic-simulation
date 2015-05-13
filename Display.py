from colorama import init, Fore, Back, Style

class Display():
    def __init__(self):
        init()
        self.clear_screen()
    
    def _print_success(self, message):
        print(Back.GREEN + Style.BRIGHT  +  Fore.BLACK + " SUCCESS " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_info(self, message):
        print(Back.BLUE + Style.BRIGHT  +  Fore.WHITE + " INFO " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_error(self, message):
        print( Back.RED + Style.BRIGHT  +  Fore.WHITE + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_network(self, message):
        print( Back.YELLOW + Style.BRIGHT  +  Fore.BLACK + " NETWORK " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_title(self, message):
        print(Fore.GREEN + Style.BRIGHT)
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("                 " + str(message))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_main_title(self, message):
        print(Fore.CYAN + Back.WHITE + Style.BRIGHT)
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(Back.RESET)
        print( "                        " + str(message).upper()+ "                     ")
        print(Back.WHITE)
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)
        
    def clear_screen(self):
        print("\033c")