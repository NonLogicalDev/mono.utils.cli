import subprocess as sp
import argparse
import json

parser = argparse.ArgumentParser()
command_parser = parser.add_subparsers(dest="cmd")

command_parser.add_parser('list-windows')
command_parser.add_parser('list-panes')
command_parser.add_parser('list-sessions')

command_parser.add_parser('reflow-windows')

class PExec(sp.Popen):
    def wait(self, **kwargs):
        super(PExec, self).wait(**kwargs)
        return self

class Tmux():
    @staticmethod
    def tmux(args):
        return PExec(['tmux'] + args, stdout=sp.PIPE, stderr=sp.PIPE)

    @staticmethod
    def cmd_list_windows():
        format = ""
        format += "{"
        format += '"idx": "#{window_id}",'
        format += '"index": "#{window_index}",'
        format += '"name": "#{window_name}",'
        format += '"layout": "#{window_layout}",'
        format += '"zoomed": #{?window_zoomed_flag,true,false},'
        format += '"active": #{?window_active,true,false}'
        format += "}"

        cmd_out = Tmux.tmux(['list-windows', '-F', format]).wait().stdout.read()
        out = "[{}]".format(
            ",".join(
                filter(
                    lambda l: len(l) > 0, cmd_out.split("\n")
                )
            )
        )
        return json.loads(out)

    @staticmethod
    def cmd_move_window(idx_a, idx_b):
        Tmux.tmux(['move-window', '-s', str(idx_a), '-t', str(idx_b)])

    @staticmethod
    def cmd_swap_window(idx_a, idx_b):
        Tmux.tmux(['move-window', '-s', str(idx_a), '-t', str(idx_b)])

    @staticmethod
    def cmd_select_window(idx):
        Tmux.tmux(['select-window', '-t', ':%s' % idx])

    @staticmethod
    def action_reflow_windows():
        wins = enumerate(sorted(Tmux.cmd_list_windows(), key=lambda w: w['index']), start=1)
        active_window = None
        for idx, win in wins:
            if win['active']:
                active_window = idx

            src_i, des_i = win['index'], idx
            if src_i != des_i:
                Tmux.cmd_move_window(src_i, des_i)
        if active_window:
            Tmux.cmd_select_window(active_window)


def main():
    args = parser.parse_args()

    if args.cmd == 'list-windows':
        print(json.dumps(Tmux.cmd_list_windows(), indent=4))

    elif args.cmd == 'reflow-windows':
        Tmux.action_reflow_windows()


if __name__ == '__main__':
    main()
