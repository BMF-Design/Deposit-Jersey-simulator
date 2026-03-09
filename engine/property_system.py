class PropertySystem:
    def __init__(self):
        self.health = {
            "structure": 100,
            "plumbing": 100,
            "heating": 100,
            "interior": 100,
        }

    def overall_health(self) -> float:
        return sum(self.health.values()) / len(self.health)

    def clamp(value, min_v, max_v):
        return max(min_v, min(value, max_v))

    def damage(self, key: str, amount: int):
        if key in self.health:
            self.health[key] -= amount
            self.clamp(key)

    def repair(self, key: str, amount: int):
        if key in self.health:
            self.health[key] += amount
            self.clamp(key)