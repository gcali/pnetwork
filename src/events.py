#!/usr/bin/env python3

NEXT_ID = 0

def _generate_id():
    global NEXT_ID
    local_id = NEXT_ID
    NEXT_ID += 1
    return local_id

class Event:
    ID = _generate_id()

def _check_arg_len(name, req, giv):
    if req != giv:
        raise TypeError(
            "{} requires {} position arguments, got {}".format(
                name,
                req,
                giv
            )
        )

def _check_duplicates(name, key, kwargs):
    if key in kwargs:
        raise TypeError(
            "{} got multiple values for {}".format(
                name,
                key
            )
        )

def _generate_init(named_attributes):
    def init(self, *args, **kwargs):
        name=type(self).__name__
        _check_arg_len(name, len(named_attributes), len(args))
        for (k,v) in zip(named_attributes,args):
            _check_duplicates(name,k,kwargs)
            setattr(self,k,v)
        for (k,v) in kwargs.items():
            setattr(self,k,v)
    return init

def _generate_docstring(name, named_attributes):
    attribute_subs=["{"+str(i)+"}" for i in range(len(named_attributes))]
    docstring_formatter="""\
{0}({{}}) -> {0}

Create a new {0} event.

List of attributes:
{{}}""".format(name).format(",".join(attribute_subs),"\n".join(attribute_subs))
    return docstring_formatter.format(*named_attributes)

def _generate_str(name, named_attributes):
    def str(self):
        attr = ["{}:{}".format(a,getattr(self,a)) for a in named_attributes]
        return "{} [{}]".format(name, ",".join(attr))
    return str

def create_event(name, *named_attributes):
    return type(
        name,
        (Event,),
        {"ID" : _generate_id(),
        "__init__" : _generate_init(named_attributes),
        "__doc__" : _generate_docstring(name, named_attributes),
        "__str__" : _generate_str(name, named_attributes),
        "id" : property(lambda self: type(self).ID)}
    )


SendMessage = create_event("SendMessage", "message", "dest")
OpenConnection = create_event("OpenConnection", "dest")

if __name__ == '__main__':
    print(type.mro(Event))
    print(type.mro(SendMessage))
    print(Event.ID)
    print(SendMessage.ID)

    s=SendMessage("I'm the message", "I'm the destination", extra="I'm extra")
    OpenConnection("I'm the destination")

    print(s.message)
    print(s.extra)
    print(s.id)

    print(s)
