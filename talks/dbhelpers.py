from random import randint

from django.http import HttpResponse

from auth_custom.models import User

from .models import PrivateMessage, PublicMessage

text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec aliquet, eros in laoreet pellentesque, lorem tortor egestas turpis, ac tempus odio nibh in sapien. Nunc interdum aliquet dolor, vel condimentum ante tristique eu. Etiam aliquet vel orci ac tristique. Vivamus lectus libero, consequat a fringilla pretium, porta in arcu. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus volutpat porttitor nibh, eu luctus lorem ornare et. Nullam ut purus tellus. In pretium elit quis mauris aliquam, sit amet tincidunt ligula commodo. Curabitur maximus imperdiet maximus. Aenean egestas dolor id porttitor malesuada. Ut elementum, libero ut feugiat vestibulum, odio lorem molestie sapien, ac elementum nibh lectus vel metus. Proin eleifend, ex in venenatis auctor, libero est vehicula ex, in facilisis turpis nunc ac neque. Sed bibendum lobortis enim et bibendum. Nam vel condimentum nulla, ut consectetur risus. Proin sagittis aliquet mauris, in accumsan velit fermentum id. Integer luctus vel eros ut accumsan.

Pellentesque consectetur ex turpis. Nullam in congue quam, a ornare sem. Nullam maximus convallis metus vitae ultrices. Curabitur accumsan lorem vitae felis luctus, a auctor arcu cursus. Nam nec erat tellus. Quisque aliquam blandit tristique. Nulla nunc justo, fringilla sed consectetur ac, vehicula et tellus. Sed malesuada tellus tellus, in condimentum nisi efficitur a. Nulla facilisi. Curabitur vitae elit iaculis, ultrices urna et, imperdiet quam.

Aliquam erat volutpat. Etiam maximus faucibus magna, non tempus tortor blandit et. Etiam hendrerit metus bibendum purus accumsan imperdiet. Nunc venenatis, metus eget dapibus vestibulum, felis erat interdum odio, in lobortis arcu nunc ut ipsum. Ut posuere malesuada dapibus. Morbi quis malesuada diam. Donec rhoncus, libero eget eleifend commodo, ipsum orci viverra eros, facilisis semper neque enim vitae libero. Fusce tempus rutrum magna quis dictum. Vestibulum rhoncus finibus ligula eu aliquam. Vestibulum dui mauris, laoreet quis velit eu, euismod laoreet diam. Nam mi tellus, mollis mattis elit a, blandit congue velit. In gravida erat eros, eget malesuada diam gravida eu. Sed sit amet lorem eleifend, fringilla mi tristique, tincidunt arcu. Etiam non blandit nisl. Nullam semper, erat eleifend maximus tempor, leo nisi fringilla ex, sit amet vehicula libero diam ut dolor.

Aenean vehicula eget purus ac imperdiet. Cras non sem justo. Morbi vulputate metus nec arcu convallis, vel porttitor nulla placerat. Donec turpis massa, tristique eget sollicitudin eu, tincidunt condimentum est. Praesent iaculis dictum magna, vel efficitur dolor viverra a. Nullam varius in sapien sit amet ultricies. Duis eget odio nec orci euismod accumsan. Vivamus consequat mi porta ipsum tristique, vitae venenatis tellus posuere. Nulla purus orci, facilisis non purus eget, pellentesque dignissim felis. Proin vehicula sed ligula nec accumsan. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas mollis faucibus orci, vitae malesuada purus tristique eleifend. Curabitur metus purus, elementum vitae gravida at, accumsan ut sapien. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;

Donec iaculis, dolor vitae vehicula ultricies, metus dolor accumsan ipsum, ut fermentum massa purus vitae augue. Fusce eu ultricies orci. Suspendisse vel sem facilisis, ornare erat eu, tincidunt sem. Aenean sodales dapibus blandit. Nulla facilisi. Phasellus eget magna sed lorem pretium fringilla eu ut neque. Curabitur vitae volutpat urna. Duis blandit imperdiet augue, id faucibus risus viverra sit amet. Praesent sodales tellus libero. Aenean pellentesque porttitor hendrerit. Morbi nec suscipit sem. Proin a elit quis turpis dignissim rhoncus a id urna. Cras semper convallis dapibus. Pellentesque hendrerit augue in rhoncus fermentum. """


def add_private_messages(request, u1=None, u2=None):
    user1 = User.objects.get(username=u1)
    user2 = User.objects.get(username=u2)
    for message in text.split("."):
        if randint(0, 10) % 2 == 0:
            PrivateMessage(
                sender=user1, receiver=user2, text=message
            ).save()
        else:
            PrivateMessage(
                sender=user2, receiver=user1, text=message
            ).save()
    return HttpResponse("<h1>Messages have sent!</h1>")


def add_public_messages(request, u1=None, u2=None, u3=None):
    user1 = User.objects.get(username=u1)
    user2 = User.objects.get(username=u2)
    user3 = User.objects.get(username=u3)
    for message in text.split("."):
        selector = randint(0, 10) % 3
        sender = None
        if selector == 0:
            sender = user1
        if selector == 1:
            sender = user2
        if selector == 2:
            sender = user3
        PublicMessage(sender=sender, text=message).save()
    return HttpResponse("<h1>Messages have sent!</h1>")
