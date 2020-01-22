import src
from config import ProductionConfig
import argparse


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true',
                        help='start Flask in debug mode (DANGEROUS!)')
    parser.add_argument('--port', default=5000, help='server port')
    parser.add_argument('--host', default='0.0.0.0', help='server host')
    parser.add_argument('--data_directory',
                        default='./data', help='data directory')
    parser.add_argument('--profile', action='store_true',
                        help='start Flask with profiler enabled (implies --debug, DANGEROUS!)')
    args = parser.parse_args()

    app = src.create_app(ProductionConfig)

    if not args.profile:
        app.run(debug=args.debug, port=args.port, host=args.host)
    else:
        from werkzeug.middleware.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        # Config profiler to show 30 most expensive functions
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        app.run(debug=True, port=args.port, host=args.host)
