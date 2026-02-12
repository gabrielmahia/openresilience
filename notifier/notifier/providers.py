import os
class Provider:
    def send(self, to_hash: str, channel: str, text: str) -> None:
        raise NotImplementedError
class MockProvider(Provider):
    def send(self, to_hash: str, channel: str, text: str) -> None:
        print(f"[MOCK SEND] channel={channel} to_hash={to_hash} text={text}")
class NoneProvider(Provider):
    def send(self, to_hash: str, channel: str, text: str) -> None:
        return
class TwilioProvider(Provider):
    def send(self, to_hash: str, channel: str, text: str) -> None:
        raise RuntimeError("Twilio adapter stub: store encrypted destination in meta to enable real sending.")
class AfricasTalkingProvider(Provider):
    def send(self, to_hash: str, channel: str, text: str) -> None:
        raise RuntimeError("Africa's Talking adapter stub: store encrypted destination in meta to enable real sending.")
def get_provider():
    p = os.environ.get("MSG_PROVIDER","mock").lower()
    if p == "none": return NoneProvider()
    if p == "mock": return MockProvider()
    if p == "twilio": return TwilioProvider()
    if p == "africastalking": return AfricasTalkingProvider()
    return MockProvider()
