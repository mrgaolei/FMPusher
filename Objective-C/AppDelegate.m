//
//  AppDelegate.m
//  FMPusher
//
//  Created by 高磊 on 13-1-13.
//  Copyright (c) 2013年 高磊. All rights reserved.
//

#import "AppDelegate.h"
#import "NSString+MD5.h"

@implementation AppDelegate

#pragma mark - Remote Notifications Push

- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken
{
    if (!TARGET_IPHONE_SIMULATOR) {
        NSMutableDictionary *deviceInfo =[[NSMutableDictionary alloc]initWithCapacity:0];
        // Get Bundle Info for Remote Registration (handy if you have more than one app)
        NSString *appName = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleDisplayName"];
        NSString *appVersion = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleVersion"];
        
        // Check what Notifications the user has turned on.  We registered for all three, but they may have manually disabled some or all of them.
        NSUInteger rntypes = [[UIApplication sharedApplication] enabledRemoteNotificationTypes];
        
        // Set the defaults to disabled unless we find otherwise...
        NSString *pushBadge = (rntypes & UIRemoteNotificationTypeBadge) ? @"enabled" : @"disabled";
        NSString *pushAlert = (rntypes & UIRemoteNotificationTypeAlert) ? @"enabled" : @"disabled";
        NSString *pushSound = (rntypes & UIRemoteNotificationTypeSound) ? @"enabled" : @"disabled";
        
        // Get the users Device Model, Display Name, Unique ID, Token & Version Number
        UIDevice *dev = [UIDevice currentDevice];
        
        NSString *deviceName = dev.name;
        NSString *deviceModel = dev.model;
        NSString *deviceSystemVersion = dev.systemVersion;
        
        // Prepare the Device Token for Registration (remove spaces and < >)
        NSString *devToken = [[[[deviceToken description]
                                stringByReplacingOccurrencesOfString:@"<"withString:@""]
                               stringByReplacingOccurrencesOfString:@">" withString:@""]
                              stringByReplacingOccurrencesOfString: @" " withString: @""];
        
        [deviceInfo setValue:appName forKey:@"appname"];
        [deviceInfo setValue:appVersion forKey:@"appversion"];
        [deviceInfo setValue:devToken forKey:@"devicetoken"];
        [deviceInfo setValue:deviceName forKey:@"devicename"];
        [deviceInfo setValue:deviceModel forKey:@"devicemodel"];
        [deviceInfo setValue:deviceSystemVersion forKey:@"deviceversion"];
        [deviceInfo setValue:pushBadge forKey:@"pushbadge"];
        [deviceInfo setValue:pushAlert forKey:@"pushalert"];
        [deviceInfo setValue:pushSound forKey:@"pushsound"];
#ifdef DEBUG
        [deviceInfo setValue:@"sandbox" forKey:@"development"];
#else
        [deviceInfo setValue:@"production" forKey:@"development"];
#endif
        NSString *poststr = [NSString stringWithFormat:@"%@%@%@%@%@%@%@", [deviceInfo objectForKey:@"appname"], FMPushKEY, [deviceInfo objectForKey:@"appversion"], [deviceInfo objectForKey:@"devicetoken"], [deviceInfo objectForKey:@"devicename"], [deviceInfo objectForKey:@"devicemodel"], [deviceInfo objectForKey:@"deviceversion"]];
        [deviceInfo setValue:poststr.md5 forKey:@"sign"];
#ifdef FMPushURL
        TTURLRequest *request = [TTURLRequest requestWithURL:FMPushURL delegate:self];
        request.cachePolicy = TTURLRequestCachePolicyNone;
        request.response = [[TTURLDataResponse alloc] init];
        request.httpMethod = @"POST";
        [request.parameters setDictionary:deviceInfo];
        [request send];
#endif
    }
}

- (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *)error
{
    NSLog(@"FailToRegisterForRemoteNotifications: %@", error.localizedDescription);
}

#pragma mark - TTURL

- (void)requestDidFinishLoad:(TTURLRequest*)request
{
    TTURLDataResponse *response = request.response;
    NSString *result = [[NSString alloc] initWithData:response.data encoding:4];
    NSLog(@"register result: %@", result);
}

- (void)request:(TTURLRequest*)request didFailLoadWithError:(NSError*)error
{
    NSLog(@"register fail: %@", error.localizedDescription);
}

@end
