class EventBus:
    """Custom event bus."""

    def __init__(self):
        self._subscribers = dict()

    def subscribe(self, topic: str, obj):
        """
        Subscribes `obj` to `topic`.
        
        Subscribers should have an `on_{topic}` function
        for each topic they wish to subscribe to.
        """
        if not topic in self._subscribers:
            self._subscribers[topic] = set()
        self._subscribers[topic].add(obj)
    
    def unsubscribe(self, topic: str, obj):
        if not topic in self._subscribers:
            return
        self._subscribers[topic].remove(obj)
        if len(self._subscribers[topic]) == 0:
            del self._subscribers[topic]
    
    def emit(self, topic: str, *args, **kwargs):
        if not topic in self._subscribers:
            return
        for obj in self._subscribers[topic]:
            name = f"on_{topic}"
            if hasattr(obj, name):
                mth = getattr(obj, name)
                mth(*args, **kwargs)

MAIN_BUS = EventBus()