#include <iostream>
#include <stdlib.h> 

using namespace std;

int roll()
{
	srand(time(NULL));
	int r = (1 + rand() % 6) + (1 + rand() % 6);
	return r;
}

int main()
{
	int win = 0;
	int lose = 0;
	
	cout << "Press enter to roll: ";
	cin.get();    //moves on to next line when Enter key pressed
	int firstroll = roll();
	cout << "First roll: " << firstroll << endl;
	
	if(firstroll == 7 || firstroll == 11)
	{
		win += 1;
		cout << firstroll << ", you win" << endl;
	}	
		
	else if(firstroll == 2 || firstroll == 3 || firstroll == 12)
	{
		lose += 1;
		cout << firstroll << ", you lose" << endl;
	}

	else
	{
		int mark = firstroll;
		cout << mark << " is your mark." << endl;
		bool seven = false;
		bool same = false;

		while((seven == false) && (same == false))
		{
			cout << "Press enter to roll again: ";
			cin.get();
			int nextroll = roll();

			if(nextroll == mark)
			{
				win += 1;
				cout << nextroll << ", you win" << endl;
				same = true;
			}

			else if(nextroll == 7)
			{
				lose += 1;
				cout << nextroll << ", you lose" << endl;
				seven = true;
			}

			else
			{
				cout << nextroll << ", roll again" << endl;
			}

		}

	}
	
}
