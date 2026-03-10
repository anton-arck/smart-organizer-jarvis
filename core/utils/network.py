import socket

class NetworkChecker:
    @staticmethod
    def is_connected(host="8.8.8.8", port=53, timeout=1):
        """Verifica si hay salida a internet mediante sockets."""
        try:
            socket.create_connection((host, port), timeout=timeout)
            return True
        except OSError:
            return False
