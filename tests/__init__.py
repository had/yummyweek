class FakeMealRetriever:
    def __init__(self, dishes):
        self.dishes = dishes

    def get(self):
        return self.dishes