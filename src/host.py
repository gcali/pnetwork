#!/usr/bin/env python3

import events

class Host:
    
    def __init__(self,id):
        self.id = id
        self._events = []
        self._event_handler = {}
    
    def add_event(self, event):
        self._events.append(event)

    def _handle_event(self, event):
        try:
            self._event_handler[event.id](event)
        except KeyError as e:
            pass

    def add_event_handler(self, event_id, handler):
        try:
            self._event_handler[event_id].append(handler)
        except KeyError as e:
            self._event_handler[event_id] = []
            return self.add_event_handler(event_id, handler)

if __name__ == '__main__':
    h = Host("main")
    h.add_event(events.SendMessage("message", "192.168.1.10"))
    print([str(e) for e in h._events])
