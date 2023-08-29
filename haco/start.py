import asyncio

from haco.mqtt import start_mqtt


def main():
    return asyncio.run(start_mqtt())


if __name__ == '__main__':
    main()
