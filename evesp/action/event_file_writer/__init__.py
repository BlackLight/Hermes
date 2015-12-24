from ...action import Action

class EventFileWriter(Action):
    """
    Event file writer action. On event received,
    write the serialized event on the specified file.

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, filepath):
        """
        filepath -- Path of the file that will contain the serialized event.
        In case the file already exists, the new event will be appended.
        """

        super().__init__(filepath=filepath)

    def on_event(self, event):
        with open(self.filepath, 'ab') as fp:
            fp.write(event.serialize())
        fp.close()

# vim:sw=4:ts=4:et:

