import argparse
import blocker

def init_parser() :
    parser = argparse.ArgumentParser()

    parser.add_argument( "-u", "--undo",
        help = "undo the last set of users blocked",
        action = "store_true" )

    return parser


def main() :
    args = init_parser().parse_args()

    if args.undo :
        blocker.undo_last_session()
    else :
        blocker.check_and_block_followers()


if __name__ == "__main__" :
    main()
