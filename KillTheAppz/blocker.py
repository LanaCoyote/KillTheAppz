import helper
import cPickle as pickle
import re
import sys

def get_blocked_words_file( mode ) :
    return open('blocked_patterns.txt', mode )


def get_last_run_blocked_file( mode ) :
    return open('.lastblock', mode )


def get_followers_to_check() :
    return helper.get_followers_since_last_poll()


def get_twitter_bio( u ) :
    return u.description


def block_user( u ) :
    print( "!! Blocking user: @{} !!".format( u.screen_name ) )
    helper.get_api().create_block( u.id )


def file_to_list( f ) :
    return [l.strip() for l in f.readlines() if not l.startswith( '#' )]


def check_and_block_followers() :
    print( "   Getting blocked word list..." )
    sys.stdout.flush()
    with get_blocked_words_file( 'rt' ) as f :
        blocked_word_list = file_to_list( f )

        for word in blocked_word_list :
            print( " ~ Blocked pattern loaded: {}".format( word ) )
    
    print( "   Getting followers to check..." )
    sys.stdout.flush()
    followers_to_check = get_followers_to_check()
    followers_blocked = []

    print( "   Checking {} new followers...".format( 
        len( followers_to_check ) ) )
    sys.stdout.flush()
    for follower in followers_to_check :
        for bw in blocked_word_list :
            match = re.search( bw, get_twitter_bio( follower ) )
            if match :
                # we're blocking this guy, let's save him to our list first
                followers_blocked.append( follower.id )

                # block them
                block_user( follower )
                continue

    if len( followers_blocked ) == 0 :
        print( "   No followers blocked, skipping undo file..." )
        sys.stdout.flush()
    else :
        print( "   Saving undo file..." )
        sys.stdout.flush()
        with get_last_run_blocked_file( 'wb' ) as f :
            pickle.dump( followers_blocked, f, -1 )
        print( " ~ Saved! To undo this session, run with -u" )
        sys.stdout.flush()

    print( "** All done! **" )
    print( " ~ Checked {} followers and blocked {} accounts matching {} patterns".format(
        len( followers_to_check ),
        len( followers_blocked ),
        len( blocked_word_list ) ) )
    

def undo_last_session() :
    print( "   Getting list of users blocked..." )
    sys.stdout.flush()
    users_blocked = []
    with get_last_run_blocked_file( 'rb' ) as f :
        users_blocked = pickle.load( f )

    print( "   Unblocking {} users...".format(
        len( users_blocked ) ) )
    sys.stdout.flush()
    for userid in users_blocked :
        user = helper.get_api().get_user( user_id = userid )
        print( " ~ Unblocking user: @{}".format( user.screen_name ) )
        helper.get_api().destroy_block( user_id = userid )

    print( "** All done! **" )
    print( " ~ Unblocked {} users".format( len( users_blocked ) ) )
