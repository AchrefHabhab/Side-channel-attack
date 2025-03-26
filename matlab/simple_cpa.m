%% Hardware Security
%  Authors: Athanasios Papadimitriou

%% Instructions for the lab and its report:
% You will have to deliver this MATLAB m-file containing the code, comments
% and a report, describing the code and answers to questions.

%% Description of provided data:
% 'datapoints' - each row of the array contains one power trace.
% 'plaintexts_SCA' - each row contains the 16 bytes of the plaintext which
% was encrypted and produced the power trace in the corresponding row of
% the 'datapoints' array.
% 'SubBytes' - contains a look-up table containing all possible SBOX
% results for all 8-bit numbers. The table returns the SBOX(X), where
% X = (Data XOR key)
% 'HW' - contains a look-up table containing the Hamming Weights of all
% 8-bit numbers.

%% Correlation Power Analysis 
%% Clear the memory
clear all;

%% Load the data
load('constants.mat');
load('attack_data_1.mat');

%% Select the keybyte and oscilloscope samples to attack 
keybyte = 1;
sample_start = 1;
sample_stop = size(datapoints,2);

%% Copy the relevant traces and sample points in a new array 
T = datapoints;

%% Copy the relevant plaintexts in a new vector
plaintext = plaintexts_SCA(:,keybyte);

%% Leakage model and hypothetical intermediate values
% You have to consider at least five different power models 
% 'LSB' - The power consumption follows the Least Significant Bit.
% 'MSB' - The power consumption follows the Most Significant Bit.
% 'HW' - The power consumption follows the Hamming Weight of all 8 bits. 
% 'IDENTITY' - The power consumption follows the value of the 8 bits. 
% 'YOUR_OWN_LEAKAGE_MODEL' - Create your own SCA power model
% Define the leakage power model you will use
LEAKAGE_MODEL = 'HW';% LSB, MSB, HW, IDENTITY, YOUR_OWN_LEAKAGE_MODEL

Keyhyp = [0:255];

%% Create the tables D, V, H, T
D = plaintext;
for i=1:size(Keyhyp,2)
    for j=1:size(D,1)
        V(j,i) = SubBytes(bitxor(D(j),Keyhyp(i))+1);
    end
end

H = HW(V + 1);

%% Apply Pearson's Correlation
for k = 1:size(H,2)
    for l=1:size(T,2)
        R(k,l) = corr(double(H(:,k)),T(:,l));
    end
end

%% Plot the correlations vs hypothetical keys.
figure;
plot(R);
title('Title goes here');
xlabel('Key Hypotheses');
ylabel('Correlation');

%% Plot the correlations vs sample points.
figure;
plot(transpose(R));
title('Title goes here');
xlabel('Samples');
ylabel('Correlation');