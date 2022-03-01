from command import Command
from parameter import Parameter

test_command = Command("access-list WORD$name [seq (1-4294967295)$seq] <deny|permit>$action <A.B.C.D/M$prefix [exact-match$exact]|any>")

test_command.make_command()
