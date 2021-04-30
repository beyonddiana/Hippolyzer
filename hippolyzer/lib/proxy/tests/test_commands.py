import unittest

from hippolyzer.lib.proxy.commands import handle_command, Parameter


class TestCommandHandler:
    def __init__(self):
        self.bar = None
        self.baz = None

    @handle_command("foobar", bar=str, baz=int)
    async def foo(self, _session, _region, bar, baz):
        self.bar = bar
        self.baz = baz

    @handle_command(
        "bazquux",
        x=Parameter(sep="/", parser=float),
        y=Parameter(sep="/", parser=float),
        z=Parameter(parser=float),
    )
    async def quux(self, _session, _region, x, y, z):
        self.bar = (x, y, z)

    @handle_command(
        y=str,
    )
    async def own_name(self, _session, _region, y):
        self.bar = y


class TestCommandHandlers(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.handler = TestCommandHandler()

    async def test_foo(self):
        await self.handler.foo(None, None, "foozy 1")
        self.assertEqual(self.handler.bar, "foozy")
        self.assertEqual(self.handler.baz, 1)

    async def test_quux(self):
        # Alternative command name was provided
        self.assertEqual(self.handler.quux.command.name, "bazquux")
        await self.handler.quux(None, None, "1/2/3")
        self.assertEqual(self.handler.bar, (1, 2, 3))

    async def test_own_name(self):
        self.assertEqual(self.handler.own_name.command.name, "own_name")

    async def test_bad_command(self):
        with self.assertRaises(ValueError):
            class _BadCommandHandler:
                @handle_command("foobaz")
                def bad_command(self, session, region):
                    pass
