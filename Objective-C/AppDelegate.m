//
//  AppDelegate.m
//  FMPusher
//
//  Created by mrgaolei on 13-1-13.
//  Copyright (c) 2013~2015年 mrgaolei. All rights reserved.
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
        NSString *appName = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleName"];
        NSString *appVersion = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleVersion"];
        
        NSString *pushBadge;
        NSString *pushAlert;
        NSString *pushSound;

        if ([[[UIDevice currentDevice] systemVersion] hasPrefix:@"8"]) {
            UIUserNotificationSettings *notifiSettings = [UIApplication sharedApplication].currentUserNotificationSettings;
            NSUInteger rntypes = notifiSettings.types;
            
            pushBadge = (rntypes & UIUserNotificationTypeBadge) ? @"enabled" : @"disabled";
            pushAlert = (rntypes & UIUserNotificationTypeAlert) ? @"enabled" : @"disabled";
            pushSound = (rntypes & UIUserNotificationTypeSound) ? @"enabled" : @"disabled";
        } else {
            // Check what Notifications the user has turned on.  We registered for all three, but they may have manually disabled some or all of them.
            NSUInteger rntypes = [[UIApplication sharedApplication] enabledRemoteNotificationTypes];
            
            // Set the defaults to disabled unless we find otherwise...
            pushBadge = (rntypes & UIRemoteNotificationTypeBadge) ? @"enabled" : @"disabled";
            pushAlert = (rntypes & UIRemoteNotificationTypeAlert) ? @"enabled" : @"disabled";
            pushSound = (rntypes & UIRemoteNotificationTypeSound) ? @"enabled" : @"disabled";
        }
        
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
        AFHTTPRequestOperationManager *manager = [AFHTTPRequestOperationManager manager];
        manager.responseSerializer.acceptableContentTypes = [NSSet setWithObject:@"text/html"];
        [manager POST:FMPushURL parameters:deviceInfo success:^(AFHTTPRequestOperation *operation, id responseObject) {
            NSLog(@"success:%@", responseObject);
        } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
            NSLog(@"failure:%@, %@", error.localizedDescription, operation.responseString);
        }];
#endif
    }
}

- (void)application:(UIApplication *)application didRegisterUserNotificationSettings:(UIUserNotificationSettings *)notificationSettings
{
    NSLog(@"didRegister");
}

- (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *)error
{
    NSLog(@"FailToRegisterForRemoteNotifications: %@", error.localizedDescription);
}

- (void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo NS_AVAILABLE_IOS(3_0)
{
    NSLog(@"ui:%@", userInfo);
}

@end
