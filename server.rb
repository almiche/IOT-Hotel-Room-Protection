require 'sinatra'
require 'pry'

class MyApp < Sinatra::Application
    
    def initialize(app = nil)
        super()
        @app = app 
    end
    
    configure do
        @@location = String.new
        @@sensitivity = 0
    end

    get '/api/v0.1/alarm/status' do
        if(!params[:location].nil?)
            @@location = params[:location]
        end
        @@location.to_s
    end

    get '/api/v1.0/configuration/sensitivity' do 
        if(params[:sensitivity] != 0)
            @@sensitivity = params[:sensitivity].to_i
        end
        @@sensitivity.to_s
    end
    
    get '/dankness' do 
        File.read(File.join('public','bobby.html'))
    end


    end
