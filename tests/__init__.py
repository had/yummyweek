class FakeMealRetriever:
    def __init__(self, dishes):
        self.dishes = dishes

    def get_dishes(self):
        return self.dishes
