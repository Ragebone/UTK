from typing import Any

from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey


class KeyMap:

    keys = {}

    @staticmethod
    def addKey(keyId: str, publicKey: Any) -> None:
        """


        :return: None
        """

        collision = KeyMap.keys.get(keyId, None)
        if collision is None:
            KeyMap.keys[keyId] = publicKey

    @staticmethod
    def ownKeyMap() -> dict[str, 'PublicKey']:
        """

        :return:
        """
        oldKeyMap = KeyMap.keys
        KeyMap.keys = {}
        return oldKeyMap
