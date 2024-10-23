#Colour Palatte for Labels (dark mode and light mode) for Label Widget
class colour4Widgets():
    def __init__(self):
        pass

    def findColour(self, theme : str) -> list[str]:
        if theme == "autumn":
            return ["#BF6F5F", "#9B4A3C"]
        elif theme == "cherry":
            return ["#F5B3B3", "#C85C5C"]
        elif theme == "coffee":
            return ["#825C46", "#5A3E32"]
        elif theme == "lavender":
            return ["#B19CD9", "#9370DB"]
        elif theme == "marsh":
            return ["#7DBE98", "#4E8F69"]
        elif theme == "breeze":
            return ["#4DB3C8", "#2D6D7D"]