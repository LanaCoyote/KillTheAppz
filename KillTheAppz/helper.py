import cPickle as pickle
import sys
import tweepy

Api = None
Followers = None

def get_api( force_rebuild = False ) :
    global Api

    if not Api or force_rebuild :
        auth = do_user_auth()
        if auth :
            Api = tweepy.API( auth )
        else :
            raise RuntimeError( "could not auth user" )

    return Api


def do_user_auth() :
    auth = tweepy.OAuthHandler( "qK8kinFsWU96lBW8ACv9e67yk",
        "IqTxTkFn1Ec50hXnBaABw6ZCMWyGeMWGgBSlcJV89dm3uCBibT" )

    try :
        print( "   Loading user auth info..." )
        sys.stdout.flush()
        f = open( '.authinfo', 'rb' )
        access_token = pickle.load( f )
        auth.set_access_token( access_token[0], access_token[1] )
        f.close()
        print( " ~ Access token loaded successfully!" )
        sys.stdout.flush()
    except :
        print( "   Failed to load info, doing first time auth..." )
        sys.stdout.flush()
        try :
            redirect_url = auth.get_authorization_url()
            print( " ~ Go to {} to authenticate".format(
                redirect_url ) )
            sys.stdout.flush()
            verifier = raw_input( " ~ Enter verification code:" )

            auth.get_access_token( verifier )

            f = open( '.authinfo', 'wb' )
            pickle.dump( 
                [ auth.access_token, auth.access_token_secret ],
                f,
                -1
            )
            f.close()
        except tweepy.TweepError :
            print( "!! Error authenticating user !!" )
            sys.stdout.flush()
            return None

    return auth


def get_current_followers() :
    global Followers
    if not Followers :
        Followers = get_api().followers()
    #for follower in tweepy.Cursor( get_api().followers ).items() :
    #    followers.append( follower )
    return Followers


def _get_last_poll_result_file( read_only ) :
    mode = 'rb' if read_only else 'wb'
    return open('.lastpoll',mode)


def get_previous_followers( lap = False ) :
    followers = []
    try :
        with _get_last_poll_result_file( read_only = True ) as f :
            try :
                followers = pickle.load( f )
                print( " ~ Previous poll results loaded" )
            except :
                print( " ~ Error loading previous poll results, skipping" )
    except IOError :
        print( " ~ Previous poll results not found, skipping" )

    if lap :
        with _get_last_poll_result_file( read_only = False ) as f :
            pickle.dump( 
                [follower.id for follower in get_current_followers()],
                f, -1 )

    return followers


def get_followers_since_last_poll() :
    diff = []
    pfollowers = get_previous_followers( lap = True )
    for follower in get_current_followers() :
        if not ( follower.id in pfollowers ) :
            diff.append( follower )

    return diff

