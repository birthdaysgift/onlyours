from django.db import models


class User(models.Model):
    name = models.TextField(max_length=50, primary_key=True)
    password = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Message2All(models.Model):
    date = models.DateField()
    time = models.TimeField()
    name = models.TextField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return "#{} [{} {}] {}: {}".format(self.id, self.date, self.time,
                                           self.name, self.text[:30])

    # def get_messages(self, page="LAST"):
    #     amount = 10
    #     messages = self.objects.all()
    #     pages = self.get_pages_num()
    #     on_page = {page_num: slice((page_num-1)*amount, page_num*amount) for page_num in pages}
    #     on_page["FIRST"] = on_page[1]
    #     on_page["LAST"] = on_page[pages[-1]]
    #     # | for example:
    #     # | if amount = 10 and len(messages) = 27
    #     # | the code above creates
    #     # | pages = (1, 2, 3)
    #     # | and on_page = {
    #     # |     "FIRST" : slice(1, 10),
    #     # |     1 : slice(0, 9),
    #     # |     2 : slice(10, 19),
    #     # |     3 : slice(20, 29),
    #     # |     "LAST" : slice(20, 29)
    #     # | }
    #     return messages[on_page[page]]

    # def get_pages_num(self):
    #     messages = self.objects.all()
    #     # noinspection PyTypeChecker
    #     return range(1, math.ceil(len(messages)/amount) + 1)
